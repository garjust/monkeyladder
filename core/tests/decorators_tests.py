from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.test import TestCase

from core import decorators

FIXTURES = ['fixtures/users', 'fixtures/core']


@decorators.ladder_is_active
def ladder_is_active_decorated(request, ladder_id):
    return 632


class LadderIsActiveTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.request = HttpRequest()

    def test_active_ladder_works(self):
        pass

    def test_inactive_ladder_returns_404(self):
        pass


@decorators.login_required_and_ladder_admin
def login_required_and_ladder_admin_decorated(request, ladder_id):
    return 4


class LoginRequiredAndLadderAdminTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.request = HttpRequest()

    def test_not_logged_in(self):
        self.request.user = AnonymousUser()
        self.assertTrue(isinstance(login_required_and_ladder_admin_decorated(self.request, 3), HttpResponseForbidden))

    def test_logged_in_not_watching(self):
        self.request.user = authenticate(username='user.d', password='password')
        self.assertTrue(isinstance(login_required_and_ladder_admin_decorated(self.request, 2), HttpResponseForbidden))

    def test_logged_in_not_admin(self):
        self.request.user = authenticate(username='user.c', password='password')
        self.assertTrue(isinstance(login_required_and_ladder_admin_decorated(self.request, 2), HttpResponseForbidden))

    def test_logged_in_and_admin(self):
        self.request.user = authenticate(username='user.admin', password='admin1')
        self.assertEqual(login_required_and_ladder_admin_decorated(self.request, 3), 4)


@decorators.can_view_ladder
def can_view_ladder_decorated(request, ladder_id):
    return 123


class CanViewLadderTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.request = HttpRequest()

    def test_anonymous_user_does_have_permission_for_public(self):
        self.request.user = AnonymousUser()
        self.assertEqual(can_view_ladder_decorated(self.request, 2), 123)

    def test_anonymous_user_does_not_have_permission_for_private(self):
        self.request.user = AnonymousUser()
        self.assertTrue(isinstance(can_view_ladder_decorated(self.request, 3), HttpResponseRedirect))

    def test_redirects_to_home_by_default(self):
        self.request.user = AnonymousUser()
        response = can_view_ladder_decorated(self.request, 3)
        self.assertEqual(response.get('location'), '/home/')

    def test_user_not_watching_private_does_not_have_permission(self):
        self.request.user = authenticate(username='user.d', password='password')
        self.assertTrue(isinstance(can_view_ladder_decorated(self.request, 1), HttpResponseRedirect))

    def test_user_watching_private_has_permission(self):
        self.request.user = authenticate(username='user.c', password='password')
        self.assertEqual(can_view_ladder_decorated(self.request, 1), 123)
