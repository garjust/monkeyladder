from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from accounts import logic

FIXTURES = ['fixtures/users', 'fixtures/core']

class GetUserOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_user_or_404

    def test_get_user(self):
        self.assertEqual(self.fixture(pk=1), User.objects.get(pk=1))

    def test_raise_404_if_user_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)
