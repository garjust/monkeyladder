from django.test import TestCase

from core.logic import ranks
from core.models import Ladder

FIXTURES = ['fixtures/users', 'fixtures/core']


class GetNewRankTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = ranks.get_new_rank

    def test_get_new_rank_basic_ladder(self):
        self.assertEqual(self.fixture(Ladder.objects.get(pk=2)), 6)

    def test_get_new_rank_leaderboard(self):
        self.assertEqual(self.fixture(Ladder.objects.get(pk=4)), 10)

    def test_get_new_rank_empty_ladder(self):
        self.assertEqual(self.fixture(Ladder.objects.get(pk=6)), 1)


class ValidateRankingTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = ranks.validate_ranking


class CorrectRankingTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        self.fixture = ranks.correct_ranking

    def test_correct_ranking_on_valid_ladder(self):
        ladder = Ladder.objects.get(pk=4)
        expected_ranking = [(ranked_item, ranked_item.rank) for ranked_item in ladder.ranking()]
        self.fixture(ladder)
        for ranked_item, expected_rank in expected_ranking:
            self.assertEqual(ranked_item.rank, expected_rank)

    def test_correct_ranking_with_empty_ladder(self):
        self.fixture(Ladder.objects.get(pk=6))

    def test_correct_ranking_with_invalid_ladder(self):
        ladder = Ladder.objects.get(pk=7)
        self.fixture(ladder)
        for i, ranked_item in enumerate(ladder.ranking()):
            self.assertEqual(ranked_item.rank, i + 1)
