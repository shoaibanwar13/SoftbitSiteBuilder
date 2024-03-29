# Generated by Django 5.0.2 on 2024-03-29 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0034_rename_facebook_link_profile_facebook_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=500, null=True)),
                ('phone', models.IntegerField()),
            ],
        ),
    ]
