# Generated by Django 4.2.6 on 2023-12-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0011_alter_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
