from django.contrib.auth.models import User
from django.test import TestCase

from core.logic import feeds
from core.models import Ladder, Watcher

FIXTURES = ['fixtures/users', 'fixtures/core']


class PublicLadderFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = feeds.public_ladder_feed
        self.user = User.objects.get(pk=1)

    def test_feed_should_have_public_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=False):
            if ladder.is_active:
                self.assertIn(ladder, ladders)

    def test_feed_should_not_have_private_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=True):
            self.assertNotIn(ladder, ladders)

    def test_feed_should_not_have_watched_ladders_if_user(self):
        ladders = self.fixture(user=self.user)
        for ladder in map(lambda w: w.ladder, self.user.watcher_set.all()):
            self.assertNotIn(ladder, ladders)

    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(size=0)), 0)


class WatchedLadderFeedTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = feeds.watched_ladder_feed
        self.user = User.objects.get(pk=1)

    def test_feed_should_have_watched_ladders(self):
        feed = self.fixture(self.user)
        watchers = Watcher.objects.filter(user=self.user)
        for watcher in watchers:
            if watcher.ladder.is_active:
                self.assertIn(watcher.ladder, feed)

    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(self.user, size=0)), 0)
