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
