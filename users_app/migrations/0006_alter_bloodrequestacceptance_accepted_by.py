# Generated by Django 5.1.4 on 2025-01-18 08:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0005_bloodrequestacceptance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodrequestacceptance',
            name='accepted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users_app.doner'),
        ),
    ]
