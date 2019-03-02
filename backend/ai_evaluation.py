from .models import AI
from .ai.simple_ai import SimpleAI
from .ai.basic_strategy_ai import BasicStrategyAI


def autoplay(ai_class, num_games, dealer_id, total_money):
    """
    Autoplays the game and generate data on game states, decisions, and outcomes
    :param ai_class: the AI class
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


def get_evaluation_metrics(all_bet_states, all_action_states):
    """
    Calculate evaluation metrics for the performance of the AI against the default dealer
    :param all_bet_states: return value of autoplay
    :param all_action_states: return value of autoplay
    :return: dict: evaluation metrics based on the states returned from autoplay
    """
    num_bets = len(all_bet_states)
    num_actions = len(all_action_states)
    avg_bet_payoff = sum([state["outcome"] for state in all_bet_states]) / num_bets
    avg_action_payoff = sum([state["outcome"] for state in all_action_states]) / num_actions

    return {
        "Number of bets placed": num_bets,
        "Number of actions taken": num_actions,
        "Average payoff per bet": round(avg_bet_payoff, 2),
        "Average payoff per action": round(avg_action_payoff, 2),
    }


def evaluate_ai_performance(num_games, ai_name):
    """
    Uses the autoplay function to have the AI play against the default dealer (dealer_id: 0), and return the evaluation
    metrics for the AI.
    :param num_games: int: number of games to play
    :param ai_name: string: name of the AI class
    :return: dict: evaluation metrics for the AI
    """
    if ai_name == "SimpleAI":
        ai_class = AI.simple_ai
    elif ai_name == "BasicStrategyAI":
        ai_class = AI.basic_strategy_ai
    else:
        print("AI class [{}] unsupported".format(ai_name))
        return {}

    all_bet_states, all_action_states = autoplay(
        ai_class=ai_class,
        num_games=num_games,
        dealer_id=0,
        total_money=1000,
    )

    return get_evaluation_metrics(all_bet_states, all_action_states)
