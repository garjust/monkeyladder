from django.test import TestCase

from core.logic import config
from core.models import LadderConfigurationKey

FIXTURES = ['fixtures/users', 'fixtures/core']

class GetConfigTest(TestCase):
    fixtures = FIXTURES + ['fixtures/leaderboard']

    def setUp(self):
        self.fixture = config.get_config

    def test_key_with_unconfigured_ladder(self):
        self.assertEqual(self.fixture(4, 'leaderboard.auto_take_first'), True)

    def test_single_key_returns_single_value(self):
        self.assertEqual(self.fixture(3, 'leaderboard.auto_take_first'), False)

    def test_bad_key_raises_exception(self):
        with self.assertRaises(LadderConfigurationKey.DoesNotExist):
            self.fixture(3, 'leaderboard.swap_Range')

    def test_multiple_keys_returns_dictionary(self):
        self.assertEqual(self.fixture(3, 'leaderboard.auto_take_first', 'leaderboard.swap_range'), {
            'leaderboard.auto_take_first': False, 'leaderboard.swap_range': 0,
        })

