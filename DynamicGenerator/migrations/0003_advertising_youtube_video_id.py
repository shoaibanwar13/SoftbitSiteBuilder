# Generated by Django 4.2.4 on 2024-02-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0002_category_advertising_short_discription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertising',
            name='youtube_video_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
