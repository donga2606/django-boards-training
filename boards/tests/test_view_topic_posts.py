from django.test import TestCase
from django.urls import reverse, resolve
from ..views import PostListView
from ..models import Board, Topic, Post
from django.contrib.auth.models import User

class TopicPostsViewTest(TestCase):
    def setUp(self):
        board = Board.objects.create(name='django', description='hehe')
        user = User.objects.create(username='donga', password='hello123', email='propython@gmail.com')
        topic = Topic.objects.create(board=board, starter=user, subject='hello django')
        url = reverse('topic_posts', kwargs={'pk': board.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_resolve(self):
        view = resolve('/boards/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)
