import json

from django.test import TestCase

from ...models import PlayerAction
from ..simple_ai import SimpleAI

class TestSimpleAI(TestCase):

    fixtures = ["dealers.json"]

    def test_play_game(self):
        ai = SimpleAI(dealer_id=1, total_money=1000)
        assert ai.state["dealer_id"] == 1
        assert ai.state["total_money"] == 1000

        all_bet_states, all_action_states = ai.play_game()
        assert len(all_bet_states) != 0
        assert len(all_action_states) != 0

        for bet_state in all_bet_states:
            assert bet_state["bet_amount"] == 10

        for action_state in all_action_states:
            assert action_state["action"] is PlayerAction.stand
