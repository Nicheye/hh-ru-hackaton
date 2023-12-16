# Generated by Django 4.2.6 on 2023-12-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0008_remove_event_tags_eventtag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habrcounter', models.PositiveIntegerField(default=0)),
                ('ytcounter', models.PositiveIntegerField(default=0)),
                ('tgcounter', models.PositiveIntegerField(default=0)),
                ('vkcounter', models.PositiveIntegerField(default=0)),
                ('foreign', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]