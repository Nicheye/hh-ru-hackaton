# Generated by Django 4.2.6 on 2023-12-16 21:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0014_profile_wins_alter_event_date_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateField(default=datetime.date(2023, 12, 12)),
        ),
        migrations.AlterField(
            model_name='eventreact',
            name='date',
            field=models.DateField(default=datetime.date(2023, 12, 8)),
        ),
    ]
