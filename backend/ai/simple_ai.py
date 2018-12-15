from ..models import PlayerAction
from .base_ai import BaseAI


class SimpleAI(BaseAI):


    def decide_bet_amount(self):
        return min(self.state["total_money"], 10)


    def decide_action(self, valid_actions):
        return PlayerAction.stand
