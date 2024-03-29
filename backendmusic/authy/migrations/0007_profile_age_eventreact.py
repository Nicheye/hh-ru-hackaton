# Generated by Django 4.2.6 on 2023-12-16 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0006_profile_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='EventReact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('react', models.CharField(choices=[('Good', 'Good'), ('Bad', 'Bad')], default='Good', max_length=5)),
                ('message', models.CharField(max_length=500)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authy.event')),
            ],
        ),
    ]
