from django.test import TestCase
from ladders.views import pages

FIXTURES = ['fixtures/users', 'fixtures/ladders']


class HomePageTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = pages.home_page

    def test_valid_int(self):
        self.assertEqual(5, 5)
