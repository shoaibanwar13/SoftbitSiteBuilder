# Generated by Django 5.0.2 on 2024-03-22 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0013_rename_foutrth_service_portfolio_fourth_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='About_Work_History',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='Second_Client_Name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='Your_Slogan',
            field=models.CharField(max_length=255, null=True),
        ),
    ]