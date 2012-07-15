from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import TestCase

from core import logic
from core.models import Ladder, Watcher, Favorite

class GetLadderOr404Test(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = logic.get_ladder_or_404
        
    def test_get_ladder(self):
        self.assertEqual(self.fixture(pk=1), Ladder.objects.get(pk=1))
        
    def test_raise_404_if_ladder_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)
        
class CanViewLadderTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = logic.can_view_ladder
        self.ladder = Ladder.objects.get(pk=1)
        
    def test_does_have_permission(self):
        user = User.objects.get(pk=1)
        self.assertTrue(self.fixture(user, self.ladder))
        
    def test_does_not_have_permission(self):
        user = User.objects.get(pk=8)
        self.assertTrue(not self.fixture(user, self.ladder))
        
    def test_anonymous_user_does_not_have_permission(self):
        user = AnonymousUser()
        self.assertTrue(not self.fixture(user, self.ladder))

class PublicLadderFeedTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = logic.public_ladder_feed
        self.user = User.objects.get(pk=1)
    
    def test_feed_should_have_public_ladders(self):
        ladders = self.fixture()
        for ladder in Ladder.objects.filter(is_private=False):
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
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = logic.watched_ladder_feed
        self.user = User.objects.get(pk=1)
    
    def test_feed_should_have_watched_ladders(self):
        feed = self.fixture(self.user)
        watchers = Watcher.objects.filter(user=self.user)
        for watcher in watchers:
            self.assertIn(watcher.ladder, feed)
            
    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(self.user, size=0)), 0)
        
class FavoriteLadderFeedTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = logic.favorite_ladder_feed
        self.user = User.objects.get(pk=1)
    
    def test_feed_should_have_favorite_ladders(self):
        feed = self.fixture(self.user)
        favorites = Favorite.objects.filter(user=self.user)
        for favorite in favorites:
            self.assertIn(favorite.ladder, feed)
            
    def test_change_size_of_feed(self):
        self.assertEqual(len(self.fixture(self.user, size=0)), 0)
        
class LadderWatchersTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        self.fixture = logic.ladder_watchers

    def test_get_correct_watchers(self):
        ladder = Ladder.objects.get(pk=1)
        watchers = self.fixture(ladder)
        for watcher in Watcher.objects.filter(ladder=ladder):
            self.assertIn(watcher, watchers)
            
class LadderModelTest(TestCase):
    fixtures = ['fixtures/core']
    
    def setUp(self):
        pass

    def test_watchers(self):
        user = User.objects.get(pk=1)
        ladder = Ladder.objects.get(pk=1)
        watcher = ladder.watcher(user)