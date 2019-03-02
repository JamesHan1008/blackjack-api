from django.core.management.base import BaseCommand

from backend.ai_evaluation import evaluate_ai_performance


class Command(BaseCommand):
    """
    Autoplays an AI against the default dealer and gets the evaluation metrics for the AI.
    """

    def add_arguments(self, parser):
        parser.add_argument("-n", "--num_games", help="Number of games to play")
        parser.add_argument("-a", "--ai_name", help="Name of the AI class")

    def handle(self, *args, **options):
        num_games = int(options["num_games"])
        ai_name = options["ai_name"]

        evaluation_metrics = evaluate_ai_performance(num_games, ai_name)
        print(evaluation_metrics)
