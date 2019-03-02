from django.core.management.base import BaseCommand

from backend.autoplay import autoplay_basic_strategy_default


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("-a", "--ai", help="Name of the AI class")


    def handle(self, *args, **options):
        ai = options["ai"]

        if ai == "BasicStrategyAI":
            all_bet_states, all_action_states = autoplay_basic_strategy_default(1)
        else:
            print("AI class [{}] unsupported".format(ai))

        print(all_bet_states[0])
        print(all_action_states[0])
