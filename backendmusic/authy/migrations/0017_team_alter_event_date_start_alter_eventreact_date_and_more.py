# Generated by Django 4.2.6 on 2023-12-16 22:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0016_alter_event_date_start_alter_eventreact_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateField(default=datetime.date(2023, 12, 15)),
        ),
        migrations.AlterField(
            model_name='eventreact',
            name='date',
            field=models.DateField(default=datetime.date(2023, 12, 5)),
        ),
        migrations.CreateModel(
            name='TeamPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authy.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
