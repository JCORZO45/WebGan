# Generated by Django 5.1.7 on 2025-04-25 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppGan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animals',
            name='lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppGan.lotscattle'),
        ),
    ]
