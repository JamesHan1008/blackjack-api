import random

from .models import Dealer

def _get_decks(num_decks):
    num_decks = int(num_decks)
    return num_decks * 4 * ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def _shuffle(cards):
    old_cards = cards
    new_cards = []

    while len(old_cards) > 0:
        r = random.randint(0, len(old_cards) - 1)

        card = old_cards.pop(r)
        new_cards.append(card)

    return new_cards

def _get_value(card):
    face_cards = {
        "A": 1,
        "J": 10,
        "Q": 10,
        "K": 10,
    }

    if card in face_cards:
        return face_cards[card]
    else:
        return int(card)

def _get_all_hand_values(cards):
    hand_values = [0]
    for card in cards:
        if card == "A":
                new_hand_values = []
                for v in hand_values:
                    new_hand_values.append(v + 1)
                    new_hand_values.append(v + 11)
                hand_values = new_hand_values
        else:
            for i in range(len(hand_values)):
                hand_values[i] += _get_value(card)
    return list(set(hand_values))

def _get_hand_value(cards):
    max_v = None
    for v in _get_all_hand_values(cards):
        if v <= 21:
            if max_v is None or v > max_v:
                max_v = v
    return max_v

def _is_hand_soft(cards):
    hand_value = _get_hand_value(cards)
    if not hand_value:
        return None
    else:
        return (hand_value - 10) in _get_all_hand_values(cards)

def _is_hand_busted(cards):
    return min(_get_all_hand_values(cards)) > 21

def _is_split_valid(state, cards):
    dealer = Dealer.objects.get(id=state["dealer_id"])

    if len(state["player_cards"]) >= dealer.max_split_hands:
        return False

    if len(cards) != 2:
        return False
    else:
        if _get_value(cards[0]) == _get_value(cards[1]):
            if cards[0] == "A" and not dealer.allow_resplit_aces and state["did_split_aces"]:
                return False
            return True
        else:
            return False

def _is_double_valid(state):
    allow_double_after_split = Dealer.objects.get(id=state["dealer_id"]).allow_double_after_split
    if len(state["player_cards"]) > 1 and not allow_double_after_split:
        return False
    else:
        return True

def start_game(dealer_id):
    num_decks = Dealer.objects.get(id=dealer_id).decks

    deck = _get_decks(num_decks)
    deck = _shuffle(deck)

    return {
        "deck": deck,
    }

def start_round(state, bet_amount):
    dealer = Dealer.objects.get(id=state["dealer_id"])

    state["dealer_cards"] = [state["deck"].pop()]
    state["player_cards"] = [[state["deck"].pop(), state["deck"].pop()]]
    state["hole_card"] = state["deck"].pop()
    state["current_hand"] = 0
    state["hand_finished"] = [False]
    state["hand_is_doubled"] = [False]
    state["messages"] = [""]

    state["is_split_valid"] = _is_split_valid(state, state["player_cards"][0])
    state["is_double_valid"] = True

    try:
        bet_amount = int(bet_amount)
    except Exception as e:
        raise Exception(e)

    state["bet_amount"] = bet_amount
    state["total_money"] -= bet_amount
    state["is_in_round"] = True

    if dealer.allow_insurance and state["dealer_cards"][0] == "A":
        state["is_insurance_valid"] = True
        return state

    state = _check_blackjacks(state)

    if dealer.allow_surrender and state["is_in_round"]:
        state["is_surrender_valid"] = True

    return state

def _continue_round(state):
    dealer = Dealer.objects.get(id=state["dealer_id"])

    state = _check_blackjacks(state)

    if dealer.allow_surrender and state["is_in_round"]:
        state["is_surrender_valid"] = True

    return state

def _finish_round(state):
    state["dealer_cards"].append(state["hole_card"])

    hands_are_busted = [_is_hand_busted(hand) for hand in state["player_cards"]]
    if all(hands_are_busted):
        state["dealer_message"] = "Dealer cards: {}".format(state["dealer_cards"])
        state["is_in_round"] = False
        return state

    state["deck"], state["dealer_cards"] = _dealer_take_action(
        state["deck"],
        state["dealer_cards"],
        state["dealer_id"],
    )

    total_money_won = 0
    for h in range(len(state["player_cards"])):
        money_won, message = _determine_winner(state["dealer_id"], state["dealer_cards"], state["player_cards"][h])

        if state["hand_is_doubled"][h]:
            total_money_won += (2 * money_won)
        else:
            total_money_won += money_won

        state["messages"][h] = message
    
    state["dealer_message"] = "Dealer cards: {}".format(state["dealer_cards"])
    state["total_money"] += total_money_won * state["bet_amount"]
    state["is_in_round"] = False

    return state

def _dealer_take_action(deck, dealer_cards, dealer_id):
    dealer = Dealer.objects.get(id=dealer_id)

    stop = False
    while not stop:
        dealer_cards.append(deck.pop())

        if _is_hand_busted(dealer_cards):
            stop = True
        elif _get_hand_value(dealer_cards) > 17:
            stop = True
        elif _get_hand_value(dealer_cards) == 17 and _is_hand_soft(dealer_cards):
            stop = not dealer.hits_soft_17

    return (deck, dealer_cards)

def _determine_winner(dealer_id, dealer_cards, player_cards):
    dealer = Dealer.objects.get(id=dealer_id)

    if _is_hand_busted(player_cards):
        message = "Player busted."
        money_won = 0
    elif _is_hand_busted(dealer_cards):
        message = "Dealer busted."
        money_won = 2
    else:
        player_value = _get_hand_value(player_cards)
        dealer_value = _get_hand_value(dealer_cards)

        if player_value > dealer_value:
            message = "Player won."
            money_won = 2
        elif player_value < dealer_value:
            message = "Dealer won."
            money_won = 0
        elif dealer.dealer_wins_ties:
            message = "Dealer wins ties."
            money_won = 0
        else:
            message = "Push."
            money_won = 1

    message += " Player cards: {}".format(player_cards)

    return money_won, message

def _check_blackjacks(state):
    dealer = Dealer.objects.get(id=state["dealer_id"])
    dealer_cards = [state["dealer_cards"][0], state["hole_card"]]
    player_cards = state["player_cards"][0]

    is_dealer_bj = _get_hand_value(dealer_cards) == 21
    is_player_bj = _get_hand_value(player_cards) == 21

    if not is_dealer_bj and not is_player_bj:
        return state

    if is_dealer_bj and is_player_bj:
        if dealer.dealer_wins_ties:
            state["messages"][0] = "Dealer wins ties. Player cards: {}".format(player_cards)
            money_won = 0
        else:
            state["messages"][0] = "Push. Player cards: {}".format(player_cards)
            money_won = 1
    elif is_dealer_bj:
        state["messages"][0] = "Dealer got blackjack. Player cards: {}".format(player_cards)
        money_won = 0
    elif is_player_bj:
        state["messages"][0] = "Player got blackjack. Player cards: {}".format(player_cards)
        money_won = 1 + dealer.blackjack_payout
    else:
        raise Exception("Unexpected error")

    state["dealer_message"] = "Dealer cards: {}".format(dealer_cards)
    state["total_money"] += money_won * state["bet_amount"]
    state["is_in_round"] = False

    return state

def player_hit(state):
    h = state["current_hand"]
    state["player_cards"][h].append(state["deck"].pop())

    if _is_hand_busted(state["player_cards"][h]):
        state["hand_finished"][h] = True
        state["messages"][h] = "Player busted. Player cards: {}".format(state["player_cards"][h])

        if all(state["hand_finished"]):
            state = _finish_round(state)
        else:
            state["current_hand"] = h + 1
            state["is_split_valid"] = _is_split_valid(state, state["player_cards"][h + 1])
    
    state["is_surrender_valid"] = False

    return state

def player_stand(state):
    h = state["current_hand"]
    state["hand_finished"][h] = True

    if all(state["hand_finished"]):
        state = _finish_round(state)
    else:
        state["current_hand"] = h + 1
        state["is_split_valid"] = _is_split_valid(state, state["player_cards"][h + 1])

    state["is_surrender_valid"] = False

    return state

def player_double(state):
    h = state["current_hand"]
    state["total_money"] -= state["bet_amount"]
    state["player_cards"][h].append(state["deck"].pop())
    state["hand_is_doubled"][h] = True

    if _is_hand_busted(state["player_cards"][h]):
        state["messages"][h] = "Player busted. Player cards: {}".format(state["player_cards"][h])

    state["hand_finished"][h] = True

    if all(state["hand_finished"]):
        state = _finish_round(state)
    else:
        state["current_hand"] = h + 1
        state["is_split_valid"] = _is_split_valid(state, state["player_cards"][h + 1])

    state["is_surrender_valid"] = False

    return state

def player_split(state):
    h = state["current_hand"]
    state["total_money"] -= state["bet_amount"]

    moved_card = state["player_cards"][h].pop()
    state["player_cards"].append([moved_card])
    state["hand_finished"].append(False)
    state["hand_is_doubled"].append(False)
    state["messages"].append("")

    last = len(state["player_cards"]) - 1
    state["player_cards"][h].append(state["deck"].pop())
    state["player_cards"][last].append(state["deck"].pop())

    if moved_card == "A":
        state["did_split_aces"] = True

    state["is_split_valid"] = _is_split_valid(state, state["player_cards"][h])
    state["is_double_valid"] = _is_double_valid(state)
    state["is_surrender_valid"] = False

    return state

def player_surrender(state):
    state["total_money"] += state["bet_amount"] * 0.5
    state["dealer_message"] = "Dealer cards: {}".format([state["dealer_cards"][0], state["hole_card"]])
    state["messages"][0] = "Player surrendered. Player cards: {}".format(state["player_cards"][0])
    state["is_in_round"] = False

    return state

def player_buy_insurance(state):
    state["is_insurance_valid"] = False

    if _get_hand_value(state["player_cards"][0]) == 21:
        state["total_money"] += state["bet_amount"] * 2
        state["is_in_round"] = False
        return state

    state["total_money"] -= state["bet_amount"] * 0.5

    dealer_cards = [state["dealer_cards"][0], state["hole_card"]]
    if _get_hand_value(dealer_cards) == 21:
        state["total_money"] += state["bet_amount"]

    return _continue_round(state)

def player_no_insurance(state):
    state["is_insurance_valid"] = False

    return _continue_round(state)
