# Generated by Django 5.0.2 on 2024-03-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0028_rating_created_at_alter_rating_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]