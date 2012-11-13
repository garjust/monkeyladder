from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.test import TestCase

from ladders.logic import pagination
FIXTURES = ['fixtures/users', 'fixtures/ladders']


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


class GetPageWithItemTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = pagination.get_page_with_item
        self.paginator = Paginator(User.objects.all(), 3)

    def test_get_page_with_item_when_item_in_paginator(self):
        page = self.fixture(self.paginator, 6)
        self.assertIn(User.objects.get(pk=6), page)
        self.assertEqual(page.number, 2)

    def test_first_page_returned_when_item_not_in_paginator(self):
        self.assertEqual(self.fixture(self.paginator, 9999).number, 1)
