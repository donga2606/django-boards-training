from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .form import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
# Create your views here.
class BoardListView(ListView):
    model = Board
    template_name = 'home.html'
    context_object_name = 'boards'

class TopicListView(ListView):
    template_name = 'board_topics.html'
    context_object_name = 'topics'
    paginate_by = 20
    model = Topic
    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)
    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        query = self.board.topics.order_by('-last_update').annotate(replies=Count('posts')-1)
        return query



@login_required()
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            # No se save vo model ma da note trong class Meta:Topic, fiald la subject, commit False de khoong save tranh gay loi
            # topic la object duoc tao ra: Topic(subject = request.POST['subject']
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(message=form.cleaned_data.get('message'), created_by=request.user, topic=topic)
            return redirect('topic_posts', pk=board.pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

class PostListView(ListView):
    model = Post
    template_name = 'topic_posts.html'
    context_object_name = 'posts'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views +=1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = Topic.objects.get(board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        query = self.topic.posts.order_by('created_at')
        return query



@login_required()
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(topic=topic, created_by=request.user, message=form.cleaned_data.get('message'))
            topic.last_update = timezone.now()
            topic.save()
            topic_url = reverse('topic_posts', kwargs={'pk': topic.board.pk, 'topic_pk': topic.pk})
            topic_post_url = "{url}?page={page}#{id}".format(
                url = topic_url,
                page = topic.get_page_count(),
                id = post.pk
            )
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'
    fields = ('message', )
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user, topic__board__pk=self.kwargs['pk'], topic__pk=self.kwargs['topic_pk'])
    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = timezone.now()
        post.updated_by = self.request.user
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
