# Generated by Django 5.0.2 on 2024-04-15 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0047_alter_advertising_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitepurchase',
            name='duration_days',
            field=models.IntegerField(default=30),
        ),
    ]
