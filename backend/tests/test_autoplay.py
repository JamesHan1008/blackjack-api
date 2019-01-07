import json
import random

from django.test import TestCase

from ..models import AI
from ..autoplay import autoplay


class TestAutoplay(TestCase):

    fixtures = ["dealers.json"]

    def test_autoplay(self):
        random.seed(1)

        num_games = 10
        all_bet_states, all_action_states = autoplay(
            ai_class=AI.basic_strategy_ai,
            num_games=num_games,
            dealer_id=1,
            total_money=1000,
        )

        with open("backend/tests/fixtures/expected_bet_states.json", "r") as f:
            expected_bet_states = json.load(f)
        with open("backend/tests/fixtures/expected_action_states.json", "r") as f:
            expected_action_states = json.load(f)

        assert all_bet_states == expected_bet_states
        assert all_action_states == expected_action_states

        random.seed()
