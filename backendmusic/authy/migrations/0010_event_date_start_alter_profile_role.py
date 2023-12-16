# Generated by Django 4.2.6 on 2023-12-16 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0009_redirection'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='date_start',
            field=models.DateField(default='1988-09-11'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('BACKEND', 'BACKEND'), ('UI/UX', 'UI'), ('Product manager', 'Product manager'), ('Frontend', 'Frontend'), ('Fullstack', 'Fullstack'), ('Analyst', 'Analyst')], default='Analyst', max_length=16),
        ),
    ]