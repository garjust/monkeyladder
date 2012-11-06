from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.test import TestCase

from core.logic import pagination
FIXTURES = ['fixtures/users', 'fixtures/core']


class GetPageTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = pagination.get_page
        self.paginator = Paginator(User.objects.all(), 3)

    def test_get_correct_page(self):
        page = self.fixture(self.paginator, 1)
        self.assertIn(User.objects.get(pk=1), page)
        self.assertIn(User.objects.get(pk=3), page)
        self.assertNotIn(User.objects.get(pk=4), page)

    def test_non_int_page_number_gives_first_page(self):
        page = self.fixture(self.paginator, "asdad")
        self.assertIn(User.objects.get(pk=1), page)
        self.assertIn(User.objects.get(pk=3), page)
        self.assertNotIn(User.objects.get(pk=4), page)

    def test_out_of_range_page_number_gives_first_page(self):
        page = self.fixture(self.paginator, 99999)
        self.assertIn(User.objects.get(pk=1), page)
        self.assertIn(User.objects.get(pk=3), page)
        self.assertNotIn(User.objects.get(pk=4), page)
