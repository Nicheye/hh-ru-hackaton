# Generated by Django 4.2.6 on 2023-12-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='../media/123.png', upload_to='media/avatars'),
        ),
    ]