from django.contrib.auth import authenticate
from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404, HttpRequest, HttpResponseForbidden
from django.test import TestCase

from accounts import decorators, forms, logic

FIXTURES = ['fixtures/users', 'fixtures/core']

@decorators.login_required_forbidden
def login_requred_forbidden_decorated(request):
    return 5

class LoginRequiredForbiddenTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.request = HttpRequest()

    def test_while_logged_in(self):
        self.request.user = authenticate(username='user.admin', password='admin1')
        self.assertEqual(login_requred_forbidden_decorated(self.request), 5)

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        self.assertTrue(isinstance(login_requred_forbidden_decorated(self.request), HttpResponseForbidden))

class GetUserOr404Test(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = logic.get_user_or_404

    def test_get_user(self):
        self.assertEqual(self.fixture(pk=1), User.objects.get(pk=1))

    def test_raise_404_if_user_dne(self):
        with self.assertRaises(Http404):
            self.fixture(pk=99999)

class UserProfileTest(TestCase):
    fixtures = FIXTURES

    def test_create_user_creates_profile(self):
        user = User.objects.create(username='bobthecat')
        self.assertEquals(user.get_profile().name(), 'bobthecat')

    def test_profile_name(self):
        user = User.objects.create(username='bobthecat', first_name='Bob', last_name='Carr')
        self.assertEquals(user.get_profile().name(), 'Bob Carr')

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
