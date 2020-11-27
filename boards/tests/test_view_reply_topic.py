from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from ..models import Board, Topic, Post
from ..form import PostForm
from ..views import reply_topic

class SetUpReplyTopic(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='django', description='hehe')
        self.user = User.objects.create_user(username='donga', password='123scdwd', email='hello@gmail.com')
        self.topic = Topic.objects.create(subject='Hello', starter=self.user, board=self.board)
        self.topic.posts.create(message='fuck off', created_by=self.user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTest(SetUpReplyTopic):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)
        self.login_url = reverse('login')
    def test_redirection(self):
        self.assertRedirects(self.response, f"{self.login_url}?next={self.url}")

class ReplyTopicViewTest(SetUpReplyTopic):
    def setUp(self):
        super().setUp()
        self.client.login(username='donga', password='123scdwd')
        self.response = self.client.get(self.url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_function(self):
        view = resolve('/boards/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)
    def test_form_input(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)
        self.assertContains(self.response, "<input ", 1)
        self.assertContains(self.response, "<textarea")

class SuccessfulReplyTopicTest(SetUpReplyTopic):
    def setUp(self):
        super().setUp()
        self.client.login(username='donga', password='123scdwd')
        self.response = self.client.post(self.url, {'message': 'hehehe'})
    def test_redirection(self):
        topic_posts_url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_last_post_url = f"{topic_posts_url}?page=1#2"
        self.assertRedirects(self.response, topic_last_post_url)
    def test_new_post(self):
        self.assertEqual(2, self.topic.posts.count())

class InvalidReplyTopicTest(SetUpReplyTopic):
    def setUp(self):
        super().setUp()
        self.client.login(username='donga', password='123scdwd')
        self.response = self.client.post(self.url, {})
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_form(self):
        form = self.response.context.get('form')
        self.assertFalse(form.is_valid())


