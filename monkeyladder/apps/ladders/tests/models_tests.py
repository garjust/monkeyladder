from django.test import TestCase

FIXTURES = ['fixtures/users', 'fixtures/ladders']


class LadderModelTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        pass
