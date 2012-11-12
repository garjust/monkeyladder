from django.contrib.auth.models import User
from django.test import TestCase

FIXTURES = ['fixtures/users', 'fixtures/ladders']

class UserProfileTest(TestCase):
    fixtures = FIXTURES

    def test_create_user_creates_profile(self):
        user = User.objects.create(username='bobthecat')
        self.assertEquals(user.get_profile().name(), 'bobthecat')

    def test_profile_name(self):
        user = User.objects.create(username='bobthecat', first_name='Bob', last_name='Carr')
        self.assertEquals(user.get_profile().name(), 'Bob Carr')