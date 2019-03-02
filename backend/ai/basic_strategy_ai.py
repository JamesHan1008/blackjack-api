import pandas as pd

from ..models import Dealer, PlayerAction
from ..game_controller import _get_value, _is_hand_soft, _get_hand_value
from .simple_ai import SimpleAI


class BasicStrategyAI(SimpleAI):
    """
    An AI that plays according to the basic optimal strategy based on the dealer's revealed card and the player's cards.
    """

    STRATEGIES_PATH = "backend/ai/strategies/"

    def __init__(self, dealer_id, total_money):
        super().__init__(dealer_id, total_money)
        self.strategy = self._get_strategy()


    def _get_strategy(self):
        if self.state["decks"] < 4 or self.state["decks"] > 8:
            return None
        else:
            if self.state["hits_soft_17"]:
                return {
                    "hard": self._read_strategy_csv("decks_4_to_8/soft_17_hit_hard.csv"),
                    "soft": self._read_strategy_csv("decks_4_to_8/soft_17_hit_soft.csv"),
                    "split": self._read_strategy_csv("decks_4_to_8/soft_17_hit_split.csv"),
                }
            else:
                return {
                    "hard": self._read_strategy_csv("decks_4_to_8/soft_17_stand_hard.csv"),
                    "soft": self._read_strategy_csv("decks_4_to_8/soft_17_stand_soft.csv"),
                    "split": self._read_strategy_csv("decks_4_to_8/soft_17_stand_split.csv"),
                }


    def _read_strategy_csv(self, file_path):
        return pd.read_csv("{}/{}".format(self.STRATEGIES_PATH, file_path), index_col=0).to_dict()


    def _interpret_action(self, action, valid_actions):
        if action == "H":
            return PlayerAction.hit
        elif action == "S":
            return PlayerAction.stand
        elif action == "P":
            if PlayerAction.split not in valid_actions:
                raise Exception("Split not in valid actions")
            return PlayerAction.split
        elif action == "Dh":
            if PlayerAction.double in valid_actions:
                return PlayerAction.double
            else:
                return PlayerAction.hit
        elif action == "Ds":
            if PlayerAction.double in valid_actions:
                return PlayerAction.double
            else:
                return PlayerAction.stand
        elif action == "Ph":
            dealer = Dealer.objects.get(id=self.dealer_id)
            if dealer.allow_double_after_split:
                if PlayerAction.split not in valid_actions:
                    raise Exception("Split not in valid actions")
                return PlayerAction.split
            else:
                return PlayerAction.hit
        elif action == "Rh":
            if PlayerAction.surrender in valid_actions:
                return PlayerAction.surrender
            else:
                return PlayerAction.hit
        elif action == "Rs":
            if PlayerAction.surrender in valid_actions:
                return PlayerAction.surrender
            else:
                return PlayerAction.stand
        elif action == "Rp":
            if PlayerAction.surrender in valid_actions:
                return PlayerAction.surrender
            else:
                if PlayerAction.split not in valid_actions:
                    raise Exception("Split not in valid actions")
                return PlayerAction.split
        else:
            raise Exception("Invalid action: {}".format(action))


    def decide_action(self, valid_actions):
        if self.strategy is None:
            return PlayerAction.stand
        else:
            player_cards = self.state["player_cards"][self.state["current_hand"]]
            dealer_card = self.state["dealer_cards"][0]

            if len(player_cards) == 2 and _get_value(player_cards[0]) == _get_value(player_cards[1]):
                action = self.strategy["split"][dealer_card][_get_value(player_cards[0])]
            elif _is_hand_soft(player_cards):
                action = self.strategy["soft"][dealer_card][_get_hand_value(player_cards)]
            else:
                action = self.strategy["hard"][dealer_card][_get_hand_value(player_cards)]

            return self._interpret_action(action, valid_actions)
