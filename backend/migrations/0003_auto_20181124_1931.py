# Generated by Django 2.1.2 on 2018-11-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20181110_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='blackjack_payout',
            field=models.FloatField(default=1.5),
        ),
    ]
