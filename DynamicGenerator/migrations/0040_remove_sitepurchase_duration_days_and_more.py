# Generated by Django 5.0.2 on 2024-04-08 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0039_sitepurchase_duration_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitepurchase',
            name='duration_days',
        ),
        migrations.AddField(
            model_name='sitepurchase',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]