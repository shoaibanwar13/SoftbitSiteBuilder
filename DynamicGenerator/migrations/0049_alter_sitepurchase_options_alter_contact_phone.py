# Generated by Django 5.0.2 on 2024-04-15 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0048_alter_sitepurchase_duration_days'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitepurchase',
            options={'verbose_name_plural': 'Site Purchase'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(max_length=16, null=True),
        ),
    ]