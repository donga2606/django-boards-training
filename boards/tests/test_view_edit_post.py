from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Topic, Post
from django.contrib.auth.models import User
class SetUpPostUpdateViewTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='django', description='hehe')
        self.username = 'donga123'
        self.password = 'djcsk122'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='donga.ftu2@gmail.com')
        self.topic = Topic.objects.create(subject='django is funny', starter=self.user, board=self.board)
        self.post = Post.objects.create(message='hello', created_by=self.user, topic=self.topic)
        self.edit_post_url = reverse('edit_post', kwargs={
            'pk': self.board.pk, 'topic_pk': self.topic.pk, 'post_pk': self.post.pk
        })

class LoginRequiredPostUpdateView(SetUpPostUpdateViewTest):
    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.edit_post_url)
    def test_login_required(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, f'{login_url}?next={self.edit_post_url}')
class UnauthorizedUserAndWrongUrlPostUpdateView(SetUpPostUpdateViewTest):
    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username='hientran', password='hello', email='hien@gmail.com')
        self.client.login(username='hientran', password='hello')
        self.response = self.client.get(self.edit_post_url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)
    def test_wrong_kwargs(self):
        board_2 = Board.objects.create(name='python', description='huhu')
        self.client.login(username=self.username, password=self.password)
        url = reverse('edit_post', kwargs={'pk': board_2.pk, 'topic_pk': self.topic.pk, 'post_pk': self.post.pk})
        # Wrong url but still have the same result
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

class PostUpdateView(SetUpPostUpdateViewTest):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.edit_post_url)
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
