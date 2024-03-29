# Generated by Django 5.0.2 on 2024-03-22 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0014_portfolio_about_work_history_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='Linked_In_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='About_Work_History',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='First_Clent_Image',
            field=models.ImageField(help_text='Please Use Small Image That Display In template ', upload_to='ClientImage/'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='Second_Clent_Image',
            field=models.ImageField(help_text='Please Use Small Image That Display In template ', upload_to='ClientImage/'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='Third_Clent_Image',
            field=models.ImageField(help_text='Please Use Small Image That Display In template ', upload_to='ClientImage/'),
        ),
    ]
