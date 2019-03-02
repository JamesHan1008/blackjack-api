from ..models import PlayerAction
from .base_ai import BaseAI


class SimpleAI(BaseAI):
    """
    A simple AI that only makes bets of 10 and stands on all hands.
    """


    def decide_bet_amount(self):
        return min(self.state["total_money"], 10)


    def decide_action(self, valid_actions):
        return PlayerAction.stand
