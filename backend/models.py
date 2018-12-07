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
