from copy import deepcopy
from abc import ABC, abstractmethod

from ..models import Dealer, PlayerAction
from ..game_controller import *


class BaseAI(ABC):


    def __init__(self, dealer_id, total_money):
        self.initiate_state(dealer_id, total_money)
        self._add_dealer_rules()
        self.min_cards_in_deck = 20


    def initiate_state(self, dealer_id, total_money):
        self.state = {
            "dealer_id": dealer_id,

            "deck": [],
            "dealer_cards": [],
            "player_cards": [[]],
            "hole_card": "",
            "current_hand": "",
            "hand_finished": [],
            "hand_is_doubled": [],
            "is_split_valid": False,
            "is_double_valid": False,
            "is_surrender_valid": False,
            "is_insurance_valid": False,
            "did_split_aces": False,
            "did_buy_insurance": False,

            "total_money": total_money,
            "bet_amount": 0,
            "is_in_game": False,
            "is_in_round": False,
            "dealer_message": "",
            "messages": [""],
        }


    def _add_dealer_rules(self):
        dealer = Dealer.objects.get(id=self.state["dealer_id"])
        self.state.update(dealer.get_rules_dict())


    def _get_valid_actions(self):
        actions = [PlayerAction.hit, PlayerAction.stand]
        if self.state["is_split_valid"]:
            actions.append(PlayerAction.split)
        if self.state["is_double_valid"]:
            actions.append(PlayerAction.double)
        if self.state["is_surrender_valid"]:
            actions.append(PlayerAction.surrender)
        if self.state["is_insurance_valid"]:
            actions.append(PlayerAction.buy_insurance)

        return actions


    def play_game(self):
        self.state["is_in_game"] = True
        all_bet_states = []
        all_action_states = []
        if self.state["deck"] == []:
            self.state["deck"] = start_game(self.state["dealer_id"])["deck"]

        while self.state["is_in_game"]:
            initial_money = self.state["total_money"]
            self.state = start_round(
                state = self.state,
                bet_amount = self.decide_bet_amount(),
            )

            bet_state = {
                "state": deepcopy(self.state),
                "bet_amount": self.state["bet_amount"],
            }
            action_states = []

            while self.state["is_in_round"]:
                action = self.decide_action(valid_actions=self._get_valid_actions())

                action_states.append({
                    "state": deepcopy(self.state),
                    "action": action,
                })

                if action == PlayerAction.hit:
                    self.state = player_hit(self.state)
                elif action == PlayerAction.stand:
                    self.state = player_stand(self.state)
                elif action == PlayerAction.double:
                    self.state = player_double(self.state)
                elif action == PlayerAction.split:
                    self.state = player_split(self.state)
                elif action == PlayerAction.surrender:
                    self.state = player_surrender(self.state)
                elif action == PlayerAction.buy_insurance:
                    self.state = player_buy_insurance(self.state)
                else:
                    raise Exception("Unexpected player action")

            if self.state["total_money"] == 0 or len(self.state["deck"]) < self.min_cards_in_deck:
                self.state["is_in_game"] = False

            # Add outcome to state
            outcome = self.state["total_money"] - initial_money
            bet_state["outcome"] = outcome
            for action_state in action_states:
                action_state["outcome"] = outcome

            # Remove hidden or irrelevant fields from states
            to_remove = ["dealer_id", "deck", "hole_card", "dealer_message", "messages"]
            for field in to_remove:
                bet_state["state"].pop(field)
                for action_state in action_states:
                    action_state["state"].pop(field)

            # Store state in memory
            all_bet_states.append(bet_state)
            all_action_states.extend(action_states)

        return all_bet_states, all_action_states


    @abstractmethod
    def decide_bet_amount(self):
        return None


    @abstractmethod
    def decide_action(self, valid_actions):
        return None
