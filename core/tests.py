from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import TestCase

from core import forms, logic
from core.models import Ladder, Watcher

FIXTURES = ['fixtures/users', 'fixtures/core']

class LadderCreationFormTest(TestCase):
    fixtures = FIXTURES
    
    def setUp(self):
        self.fixture = forms.LadderCreationForm
        self.user = User.objects.get(pk=1)
        self.new_ladder = {
            'name': 'New ladder',
            'rungs': '10',
            'is_private': '0',
            'type': 'LEADERBOARD',
        }
        
    def test_success(self):
        form = self.fixture(self.new_ladder)
        form.is_valid()
        self.assertTrue(form.is_valid())
        self.assertFalse(Ladder.objects.filter(name='New Ladder'), 'Ladder should not exist')
        ladder = form.save(self.user)
        self.assertEquals(ladder.is_private, False, 'The new ladder is correct')
        self.assertEquals(ladder.created_by, self.user, 'The new ladder was created by user passed in')
        self.assertEquals(Watcher.objects.get(ladder=ladder, user=self.user).type, 'ADMIN', 'An admin watcher was created with the ladder and user')
        
class LadderRankingEditFormTest(TestCase):
    fixtures = FIXTURES
    
    def setUp(self):
        self.fixture = LadderRankingEditForm
        self.ladder = Ladder.objects.get(name='Public Basic')
        
    def test_success(self):
        form = self.fixture(ladder)

class GetLadderOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_ladder_or_404

    def test_get_ladder(self):
        self.assertEqual(self.fixture(pk=1), Ladder.objects.get(pk=1))

    def test_raise_404_if_ladder_dne(self):
        self.assertRaises(Http404, self.fixture, pk=99999)

class CanViewLadderTest(TestCase):
    fixtures = FIXTURES

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
    fixtures = FIXTURES

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
    fixtures = FIXTURES

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

class LadderWatchersTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.ladder_watchers

    def test_get_correct_watchers(self):
        ladder = Ladder.objects.get(pk=1)
        watchers = self.fixture(ladder)
        for watcher in Watcher.objects.filter(ladder=ladder):
            self.assertIn(watcher, watchers)

class LadderModelTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        pass

    def test_watchers(self):
        user = User.objects.get(pk=1)
        ladder = Ladder.objects.get(pk=1)
        watcher = ladder.watcher(user)
