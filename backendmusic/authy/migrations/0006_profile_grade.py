# Generated by Django 4.2.6 on 2023-12-16 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0005_event_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='grade',
            field=models.CharField(choices=[('Junior', 'Junior'), ('Middle', 'Middle'), ('Senior', 'Senior')], default='Junior', max_length=10),
        ),
    ]
