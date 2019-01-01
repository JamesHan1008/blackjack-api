import json

from django.test import TestCase

from ...models import PlayerAction
from ...tests.fixtures.decks import deck_fixtures
from ..basic_strategy_ai import BasicStrategyAI

class TestBasicStrategyAI(TestCase):

    fixtures = ["dealers.json"]

    def test_play_game1(self):
        ai = BasicStrategyAI(dealer_id=3, total_money=1000)
        ai.state["deck"] = deck_fixtures[7][:]
        ai.min_cards_in_deck = 1

        all_bet_states, all_action_states = ai.play_game()
        assert [action_state["action"] for action_state in all_action_states] == [
            PlayerAction.hit, PlayerAction.double
        ]
        assert [action_state["outcome"] for action_state in all_action_states] == [-20, -20]
        assert [bet_state["outcome"] for bet_state in all_bet_states] == [-20]

    def test_play_game2(self):
        ai = BasicStrategyAI(dealer_id=3, total_money=1000)
        ai.state["deck"] = deck_fixtures[8][:]
        ai.min_cards_in_deck = 1

        all_bet_states, all_action_states = ai.play_game()
        assert [action_state["action"] for action_state in all_action_states] == [
            PlayerAction.split, PlayerAction.stand, PlayerAction.double
        ]
        assert [action_state["outcome"] for action_state in all_action_states] == [10, 10, 10]
        assert [bet_state["outcome"] for bet_state in all_bet_states] == [10]
