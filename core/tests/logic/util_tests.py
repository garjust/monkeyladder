from core.logic import util
from core.models import Ladder, Watcher
from django.contrib.auth.models import AnonymousUser, User
from django.http import Http404
from django.test import TestCase

FIXTURES = ['fixtures/users', 'fixtures/core']


class IntOr404Test(TestCase):

    def setUp(self):
        self.fixture = util.int_or_404

    def test_valid_int(self):
        self.assertEqual(self.fixture("23"), 23)

    def test_raise_404_if_int_invalid(self):
        with self.assertRaises(Http404):
            self.fixture("sad")


class IntOrNoneTest(TestCase):

    def setUp(self):
        self.fixture = util.int_or_none

    def test_valid_int(self):
        self.assertEqual(self.fixture("12"), 12)

    def test_returns_none_with_invalid_int(self):
        self.assertEqual(self.fixture("sasd"), None)


class EmptyStringIfNone(TestCase):

    def setUp(self):
        self.fixture = util.empty_string_if_none

    def test_empty_string_returned_when_none(self):
        self.assertEqual(self.fixture(None), "")

    def test_input_returned_if_not_none(self):
        self.assertEqual(self.fixture("asd"), "asd")
        self.assertEqual(self.fixture(32), 32)
        self.assertEqual(self.fixture([1, 2]), [1, 2])


class GetLadderOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = util.get_ladder_or_404

    def test_get_ladder(self):
        self.assertEqual(self.fixture(pk=1), Ladder.objects.get(pk=1))

    def test_raise_404_if_ladder_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)


class GetWatcherTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = util.get_watcher

    def return_none_if_anonymous_user(self):
        self.assertEqual(self.fixture(AnonymousUser(), 4), None)

    def return_none_if_no_watcher(self):
        self.assertEqual(self.fixture(User.objects.get(pk=7), 3), None)

    def return_watcher_if_exists(self):
        self.assertEqual(self.fixture(User.objects.get(pk=6), 3), Watcher.objects.get(user=6, ladder=3))

    def return_none_if_watcher_not_correct_type(self):
        self.assertEqual(self.fixture(User.objects.get(pk=6), 3, 'ADMIN'), None)

    def return_watcher_if_watcher_correct_type(self):
        self.assertEqual(self.fixture(User.objects.get(pk=1), 3, 'ADMIN'), Watcher.objects.get(user=1, ladder=3))
