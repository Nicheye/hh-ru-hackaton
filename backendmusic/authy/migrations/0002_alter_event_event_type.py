# Generated by Django 4.2.6 on 2023-12-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('Hackaton', 'Hackaton'), ('Meetup', 'Meetup')], default='123', max_length=12),
        ),
    ]
