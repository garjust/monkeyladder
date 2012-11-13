from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponseForbidden
from django.test import TestCase

from accounts import decorators

FIXTURES = ['fixtures/users', 'fixtures/ladders']

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