from django.contrib.auth.models import User
from django.test import TestCase

from core import forms
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
        self.assertEqual(ladder.is_private, False, 'The new ladder is correct')
        self.assertEqual(ladder.created_by, self.user, 'The new ladder was created by user passed in')
        self.assertEqual(Watcher.objects.get(ladder=ladder, user=self.user).type, 'ADMIN', 'An admin watcher was created with the ladder and user')

class LadderRankingEditFormTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = forms.LadderRankingEditForm
        self.ladder = Ladder.objects.get(name='Public Basic')

    def test_success(self):
        self.assertTrue(False, 'NO TESTS HERE')

class LadderConfigurationFormTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = forms.LadderConfigurationForm
        self.ladder = Ladder.objects.get(name='Private Basic')

    def test_success(self):
        form = self.fixture(self.ladder)
        self.assertIs(form['name'].value(), self.ladder.name)
        form_dictionary = {
            'name': 'Private Basic Configured',
            'is_private': '0',
        }
        form = self.fixture(self.ladder, form_dictionary)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.ladder.name, 'Private Basic Configured')
        self.assertFalse(self.ladder.is_private)
        self.assertEqual(self.ladder.rungs, 25)