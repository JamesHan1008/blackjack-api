from .fixtures.decks import deck_fixtures

def get_beginning_state(dealer_id, deck_id):
    return {
        "dealers": [],
        "dealer_id": dealer_id,
        "dealer": {},

        "deck": deck_fixtures[deck_id][:],
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

        "total_money": 1000,
        "bet_amount": 0,
        "is_in_game": False,
        "is_in_round": False,
        "dealer_message": "",
        "messages": [""],
    }
