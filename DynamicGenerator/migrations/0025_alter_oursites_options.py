# Generated by Django 5.0.2 on 2024-03-26 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0024_sitepurchase_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='oursites',
            options={'ordering': ('-date',), 'verbose_name_plural': 'Softbit Websites Templates'},
        ),
    ]
