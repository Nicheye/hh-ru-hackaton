# Generated by Django 4.2.6 on 2023-12-16 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0010_event_date_start_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateField(default='1978-08-03'),
        ),
        migrations.AlterField(
            model_name='eventtag',
            name='tags',
            field=models.CharField(blank=True, choices=[('BACKEND', 'BACKEND'), ('UI/UX', 'UI'), ('Product manager', 'Product '), ('Frontend', 'Frontend'), ('Fullstack', 'Fullstack'), ('Analyst', 'Analyst')], default='Fullstack', max_length=30),
        ),
    ]
