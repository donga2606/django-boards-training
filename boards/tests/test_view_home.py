from django.test import TestCase
from django.urls import reverse, resolve
from ..views import *
from ..models import Board, Topic, Post
# Create your tests here.
class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='django', description='hi hi')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_view_function(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_links_to_topics(self):
        topic_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(topic_url))