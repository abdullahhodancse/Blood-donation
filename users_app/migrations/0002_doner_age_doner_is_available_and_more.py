# Generated by Django 5.1.4 on 2025-01-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doner',
            name='age',
            field=models.PositiveIntegerField(default=18),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doner',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='doner',
            name='last_donation_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
