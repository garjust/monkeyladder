from django.contrib.auth.models import User
from django.test import TestCase

from accounts import forms
FIXTURES = ['fixtures/users', 'fixtures/core']


class ExtendedUserCreationFormTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = forms.ExtendedUserCreationForm
        self.new_user = {
            'username': 'bobthecat',
            'password1': 'password',
            'password2': 'password',
            'first_name': 'Bob',
            'last_name': 'Carr',
            'email': 'bobthecat@roar.net',
        }

    def test_success(self):
        form = self.fixture(self.new_user)
        self.assertTrue(form.is_valid())
        self.assertFalse(User.objects.filter(username='bobthecat'), 'User bobthecat should not exist')
        user = form.save()
        self.assertEquals(user.username, 'bobthecat', 'The new user has username bobthecat')

    def test_mismatched_passwords(self):
        self.new_user['password2'] = 'passWord'
        form = self.fixture(self.new_user)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        self.assertIn('password2', form.errors)

    def test_empty_fields_first_name(self):
        del self.new_user['first_name']
        form = self.fixture(self.new_user)
        self.assertFalse(form.is_valid(), 'Form should not be valid')
        self.assertIn('first_name', form.errors)
