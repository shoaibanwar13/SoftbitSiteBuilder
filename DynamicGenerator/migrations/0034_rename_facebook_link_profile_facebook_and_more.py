# Generated by Django 5.0.2 on 2024-03-27 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0033_profile_facebook_link_profile_linkedin_link_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='facebook_link',
            new_name='facebook',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='linkedin_link',
            new_name='linkedin',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='skypelink',
            new_name='skype',
        ),
    ]