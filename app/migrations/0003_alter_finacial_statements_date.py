# Generated by Django 5.2.3 on 2025-07-16 19:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20250716_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finacial_statements',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
