from copy import deepcopy

from django.test import TestCase

from ..game_controller import *
from ..game_controller import _get_hand_value
from .mock_game_base import *

class TestMockGames(TestCase):

    fixtures = ["dealers.json"]

    def test_mock_game1(self):
        """
        This test tests the following functions:
            start_round
            _is_split_valid   (False case)
            _check_blackjacks (when player has a blackjack)
        """
        state = get_beginning_state(dealer_id=1, deck_id=1)

        state = start_round(state, bet_amount=100)
        assert state["dealer_cards"] == ["K"]
        assert state["player_cards"] == [["A", "K"]]
        assert state["hole_card"] == "5"
        assert state["is_split_valid"] == False
        assert state["total_money"] == 1150
        assert "Player got blackjack." in state["messages"][0]
        assert state["is_in_round"] == False

    def test_mock_game2(self):
        """
        This test tests the following functions:
            start_round
            _is_split_valid   (True case)
            _check_blackjacks (when dealer has a blackjack)
        """
        state = get_beginning_state(dealer_id=1, deck_id=2)

        state = start_round(state, bet_amount=100)
        assert state["dealer_cards"] == ["K"]
        assert state["player_cards"] == [["10", "J"]]
        assert state["hole_card"] == "A"
        assert state["is_split_valid"] == True
        assert state["total_money"] == 900
        assert "Dealer got blackjack." in state["messages"][0]
        assert state["is_in_round"] == False

    def test_mock_game3(self):
        """
        This test tests the following functions:
            player_hit
            player_stand
            player_double
            player_split
            _is_split_valid (reaches max_split_hands)
            _finish_round
            _dealer_take_action
            _determine_winner
        """
        state = get_beginning_state(dealer_id=1, deck_id=3)

        state = start_round(state, bet_amount=100)
        assert state["is_split_valid"] == True
        assert state["is_in_round"] == True

        state = player_split(state)
        assert state["player_cards"] == [["2", "2"], ["2", "8"]]
        assert state["is_split_valid"] == False
        assert state["current_hand"] == 0

        state = player_hit(state)
        state = player_hit(state)
        assert state["player_cards"][0] == ["2", "2", "A", "8"]
        assert _get_hand_value(state["player_cards"][0]) == 13
        assert state["hand_finished"][0] == False

        state = player_stand(state)
        assert state["hand_finished"][0] == True
        assert state["current_hand"] == 1

        state = player_double(state)
        assert state["player_cards"][1] == ["2", "8", "Q"]
        assert _get_hand_value(state["player_cards"][1]) == 20
        assert state["hand_finished"][1] == True
        assert state["hand_is_doubled"] == [False, True]

        assert state["is_in_round"] == False
        assert state["dealer_cards"] == ["3", "5", "10"]
        assert "Dealer won." in state["messages"][0]
        assert "Player won." in state["messages"][1]
        assert state["total_money"] == 1100

    def test_mock_game4(self):
        """
        This test tests the following functions:
            _is_split_valid (when resplitting aces)
        """
        state1 = get_beginning_state(dealer_id=3, deck_id=4)
        state2 = get_beginning_state(dealer_id=4, deck_id=4)

        state1 = start_round(state1, bet_amount=100)
        state2 = start_round(state2, bet_amount=100)
        assert state1["player_cards"] == [["A", "A"]]
        assert state2["player_cards"] == [["A", "A"]]
        assert state1["is_split_valid"] == True
        assert state2["is_split_valid"] == True

        state1 = player_split(state1)
        state2 = player_split(state2)
        assert state1["player_cards"] == [["A", "A"], ["A", "A"]]
        assert state2["player_cards"] == [["A", "A"], ["A", "A"]]
        assert state1["is_split_valid"] == True
        assert state2["is_split_valid"] == False

    def test_mock_game5(self):
        """
        This test tests the following functions:
            player_buy_insurance
            player_no_insurance
        """
        state1 = get_beginning_state(dealer_id=1, deck_id=5)
        state2 = get_beginning_state(dealer_id=1, deck_id=6)

        state1 = start_round(state1, bet_amount=100)
        state2 = start_round(state2, bet_amount=100)
        assert state1["player_cards"] == [["5", "5"]]
        assert state2["player_cards"] == [["A", "Q"]]
        assert state1["dealer_cards"][0] == "A"
        assert state2["dealer_cards"][0] == "A"
        assert state1["hole_card"] == "Q"
        assert state2["hole_card"] == "Q"
        assert state1["is_insurance_valid"] == True
        assert state2["is_insurance_valid"] == True

        state1_ins = player_buy_insurance(deepcopy(state1))
        state2_ins = player_buy_insurance(deepcopy(state2))
        state1_no_ins = player_no_insurance(deepcopy(state1))
        state2_no_ins = player_no_insurance(deepcopy(state2))
        assert state1_ins["total_money"] == 950
        assert state2_ins["total_money"] == 1100
        assert state1_no_ins["total_money"] == 900
        assert state2_no_ins["total_money"] == 1000
