# Generated by Django 2.1.2 on 2018-11-24 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20181124_1931'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dealer',
            old_name='max_resplits',
            new_name='max_split_hands',
        ),
    ]