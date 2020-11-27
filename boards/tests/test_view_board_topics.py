from django.test import TestCase
from django.urls import reverse, resolve
from ..views import *
from ..models import Board, Topic, Post


class BoardTopicsTest(TestCase):
    def setUp(self):
        Board.objects.create(name='django', description='hi hi')
        url = reverse('board_topics', kwargs={'pk': 1})
        self.response = self.client.get(url)
    def test_board_topics_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 10})
        response_2 = self.client.get(url)
        self.assertEquals(response_2.status_code, 404)

    def test_board_topics_url_resolve(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)

    def test_contains_link_to_homepage_and_new_topic(self):
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{0}"'.format(homepage_url))
        self.assertContains(self.response, 'href="{0}"'.format(new_topic_url))
