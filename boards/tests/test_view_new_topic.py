from django.test import TestCase
from django.urls import reverse, resolve
from ..views import *
from ..models import Board, Topic, Post

class LogInRequiredNewTopicTest(TestCase):
    def setUp(self):
        board = Board.objects.create(name='django', description='hehe')
        self.new_topic_url = reverse('new_topic', kwargs={'pk': board.pk})
        self.login_url = reverse('login')
        self.response = self.client.get(self.new_topic_url)
    def test_redirection(self):
        self.assertRedirects(self.response, f'{self.login_url}?next={self.new_topic_url}')



class NewTopicViewTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='django', description='Hi hi')
        self.url = reverse('new_topic', kwargs={'pk': self.board.pk})
        user = User.objects.create_user(username='donga123', password='1234abcd', email='donga.ftu2@gmail.com')
        self.client.login(username='donga123', password='1234abcd')
        self.response = self.client.get(self.url)


    def test_new_topic_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_view_fail_status_code(self):
        url_test = reverse('new_topic', kwargs={'pk': 99})
        response_2 = self.client.get(url_test)
        self.assertEquals(response_2.status_code, 404)

    def test_view_resolve(self):
        view = resolve("/boards/1/new/")
        self.assertEquals(view.func, new_topic)

    def test_new_topic_contain_link_back_to_board_topics(self):
        self.assertContains(self.response, 'href="{0}"'.format(reverse('board_topics', kwargs={'pk': self.board.pk})))

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_valid_data_form(self):
        data = {
            'subject': 'hello',
            'message': 'hello'
        }
        self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)
    def test_post_form_invalid_data(self):
        response = self.client.post(self.url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

