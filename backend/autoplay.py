from .models import AI
from .ai.simple_ai import SimpleAI
from .ai.basic_strategy_ai import BasicStrategyAI


def autoplay(ai_class, num_games, dealer_id, total_money):
    """
    Autoplays the game and generate data on game states, decisions, and outcomes
    :param ai_class: instance of an AI class
    :param num_games: int: number of games to play
    :param dealer_id: int
    :param total_money: int: total money to start with
    :return:
        all_bet_states: list of dicts: each dict contains the game state before a bet, the bet amount, and the outcome
        all_action_states list of dicts: each dict contains the game state before an action, the action, and the outcome
    """
    if ai_class is AI.simple_ai:
        ai = SimpleAI(dealer_id=dealer_id, total_money=total_money)
    elif ai_class is AI.basic_strategy_ai:
        ai = BasicStrategyAI(dealer_id=dealer_id, total_money=total_money)
    else:
        raise Exception("Unsupported AI class: {}".format(ai_class))

    all_bet_states, all_action_states = [], []
    for _ in range(num_games):
        ai.initiate_state(dealer_id=dealer_id, total_money=total_money)
        bet_states, action_states = ai.play_game()
        
        all_bet_states.extend(bet_states)
        all_action_states.extend(action_states)

    return all_bet_states, all_action_states


def autoplay_basic_strategy_default(num_games):
    """
    Wrapper function for autoplay, where the BasicStrategyAI is playing against the default dealer (dealer_id: 0)
    :param num_games: int: number of games to play
    :return: same as autoplay
    """
    all_bet_states, all_action_states = autoplay(
        ai_class=AI.basic_strategy_ai,
        num_games=num_games,
        dealer_id=0,
        total_money=1000,
    )

    return all_bet_states, all_action_states
