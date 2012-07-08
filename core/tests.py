from django.test import TestCase

from django.contrib.auth.models import User
from core.models import Ladder, Watcher, Favorite
from core.logic import has_ladder_permission, public_ladder_feed, watched_ladder_feed, favorite_ladder_feed

class PublicLadderFeedTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = public_ladder_feed
    
    def test_feed_should_have_public_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=False):
            self.assertTrue(ladder in ladders)
            
    def test_feed_should_not_have_private_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=True):
            self.assertTrue(ladder not in ladders)
            
    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(size=0)), 0)
        
class WatchedLadderFeedTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = watched_ladder_feed
        self.user = User.objects.get(pk=1)
    
    def test_feed_should_have_watched_ladders(self):
        feed = self.fixture(self.user)
        watchers = Watcher.objects.filter(user=self.user)
        for watcher in watchers:
            self.assertTrue(watcher.ladder in feed)
            
    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(self.user, size=0)), 0)
        
class FavoriteLadderFeedTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = favorite_ladder_feed
        self.user = User.objects.get(pk=1)
    
    def test_feed_should_have_favorite_ladders(self):
        feed = self.fixture(self.user)
        favorites = Favorite.objects.filter(user=self.user)
        for favorite in favorites:
            self.assertTrue(favorite.ladder in feed)
            
    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(self.user, size=0)), 0)
