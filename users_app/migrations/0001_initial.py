# Generated by Django 5.1.4 on 2025-01-17 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='doner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mobile_number', models.CharField(max_length=12)),
                ('city', models.CharField(max_length=120)),
                ('Street', models.CharField(max_length=120)),
                ('other', models.TextField()),
                ('date_bath', models.DateField()),
                ('image', models.ImageField(upload_to='patient/images/')),
                ('blood_group', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users_app.bloodgroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
