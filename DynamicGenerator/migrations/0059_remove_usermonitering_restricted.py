# Generated by Django 5.0.2 on 2024-04-26 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0058_alter_deploye_sitefile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermonitering',
            name='restricted',
        ),
    ]
