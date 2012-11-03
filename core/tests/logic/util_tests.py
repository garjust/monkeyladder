from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.test import TestCase

from core.logic import util
from core.models import Ladder

FIXTURES = ['fixtures/users', 'fixtures/core']


class IntOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = util.int_or_404

    def test_valid_int(self):
        self.assertEqual(self.fixture("23"), 23)

    def test_raise_404_if_int_invalid(self):
        with self.assertRaises(Http404):
            self.fixture("sad")


class GetLadderOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = util.get_ladder_or_404

    def test_get_ladder(self):
        self.assertEqual(self.fixture(pk=1), Ladder.objects.get(pk=1))

    def test_raise_404_if_ladder_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)


class GetUserOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = util.get_user_or_404

    def test_get_user(self):
        self.assertEqual(self.fixture(pk=1), User.objects.get(pk=1))

    def test_raise_404_if_user_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)


class GetPageOrFirstPageTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = util.get_page_or_first_page
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
