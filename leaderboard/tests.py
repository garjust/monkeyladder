from django.test import TestCase

from leaderboard import logic

class AdjustRankingsTest(TestCase):
    
    def setUp(self):
        self.fixture = logic.adjust_rankings
    
    def test_simple_swap(self):
        fixtures = ['fixtures/core', 'fixtures/leaderboard']
        
        self.assertEqual(1 + 1, 2)
        raise AssertionError()