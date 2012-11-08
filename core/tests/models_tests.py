from django.test import TestCase

FIXTURES = ['fixtures/users', 'fixtures/core']


class LadderModelTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        pass
