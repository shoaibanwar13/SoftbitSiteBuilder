# Generated by Django 5.0.2 on 2024-03-26 07:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0023_withdrawl_request_bank_withdrawl_request_routing_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepurchase',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DynamicGenerator.profile'),
        ),
    ]
