# Generated by Django 5.0.2 on 2024-03-23 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0017_portfolio_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertising',
            name='category',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='category',
        ),
    ]
