# Generated by Django 5.0.2 on 2024-04-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0055_usermonitering_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepurchase',
            name='expire',
            field=models.BooleanField(default=False),
        ),
    ]