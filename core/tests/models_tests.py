from django.contrib.auth.models import User
from django.test import TestCase

from core import models

FIXTURES = ['fixtures/users', 'fixtures/core']


class LadderModelTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        pass

    def test_watchers(self):
        user = User.objects.get(pk=1)
        ladder = models.Ladder.objects.get(pk=1)
        watcher = ladder.watcher(user)
