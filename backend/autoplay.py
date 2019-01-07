from .models import AI
from .ai.simple_ai import SimpleAI
from .ai.basic_strategy_ai import BasicStrategyAI

def autoplay(ai_class, num_games, dealer_id, total_money):
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
