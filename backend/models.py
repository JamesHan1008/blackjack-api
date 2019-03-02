from enum import Enum

from django.db import models


class Dealer(models.Model):
    name                     = models.CharField(max_length=255)

    decks                    = models.IntegerField(default=2)
    blackjack_payout         = models.FloatField(  default=1.5)
    hits_soft_17             = models.BooleanField(default=True)
    allow_insurance          = models.BooleanField(default=False)
    allow_surrender          = models.BooleanField(default=False)
    max_split_hands          = models.IntegerField(default=1)
    allow_resplit_aces       = models.BooleanField(default=False)
    allow_double_after_split = models.BooleanField(default=False)
    dealer_wins_ties         = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_rules_dict(self):
        return {
            "decks": self.decks,
            "blackjack_payout": self.blackjack_payout,
            "hits_soft_17": self.hits_soft_17,
            "allow_insurance": self.allow_insurance,
            "allow_surrender": self.allow_surrender,
            "max_split_hands": self.max_split_hands,
            "allow_resplit_aces": self.allow_resplit_aces,
            "allow_double_after_split": self.allow_double_after_split,
            "dealer_wins_ties": self.dealer_wins_ties,
        }


class PlayerAction(str, Enum):
    hit = "hit"
    stand = "stand"
    double = "double"
    split = "split"
    surrender = "surrender"
    buy_insurance = "buy_insurance"

    def __str__(self):
        return self.value


class AI(Enum):
    simple_ai = "SimpleAI"
    basic_strategy_ai = "BasicStrategyAI"
