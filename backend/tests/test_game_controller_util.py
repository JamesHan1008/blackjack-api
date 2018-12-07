from ..game_controller import _get_decks, _shuffle, _get_value, _get_all_hand_values, _get_hand_value, _is_hand_soft, _is_hand_busted

hands = [
    ["A", "Q"],
    ["A", "5"],
    ["4", "K"],
    ["A", "A", "A"],
    ["A", "A", "A", "8"],
    ["A", "Q", "5"],
    ["A", "Q", "5", "9"],
    ["A", "Q", "5", "6"],
]

all_hand_values = [
    [11, 21],
    [6, 16],
    [14],
    [3, 13, 23, 33],
    [11, 21, 31, 41],
    [16, 26],
    [25, 35],
    [22, 32],
]

def test_get_decks():
    deck = _get_decks(num_decks=3)
    assert len(deck) == 3 * 52

    deck = _get_decks(num_decks="4")
    assert len(deck) == 4 * 52

def test_shuffle():
    deck = _get_decks(num_decks=3)
    num_cards = len(deck)
    new_deck = _shuffle(deck)
    assert len(deck) == 0
    assert len(new_deck) == num_cards

    deck2 = _get_decks(num_decks=3)
    new_deck2 = _shuffle(deck2)
    assert new_deck != new_deck2

def test_get_value():
    assert _get_value("A") == 1
    assert _get_value("5") == 5
    assert _get_value("J") == 10

def test_get_all_hand_values():
    for i in range(len(hands)):
        assert len(_get_all_hand_values(hands[i])) == len(all_hand_values[i])
        for v in _get_all_hand_values(hands[i]):
            assert v in all_hand_values[i]

def test_get_hand_value():
    hand_values = [_get_hand_value(hand) for hand in hands]
    assert hand_values == [21, 16, 14, 13, 21, 16, None, None]

def test_is_hand_soft():
    hand_soft = [_is_hand_soft(hand) for hand in hands]
    assert hand_soft == [True, True, False, True, True, False, None, None]

def test_is_hand_busted():
    hand_busted = [_is_hand_busted(hand) for hand in hands]
    assert hand_busted == [False, False, False, False, False, False, True, True]
