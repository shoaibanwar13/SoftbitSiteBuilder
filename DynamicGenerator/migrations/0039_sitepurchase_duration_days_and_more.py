# Generated by Django 5.0.2 on 2024-04-08 04:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0038_alter_hospital_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitepurchase',
            name='duration_days',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Doctor_Image',
            field=models.ImageField(help_text='Informative Image Of Doctor', upload_to='doctor_images/'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Email',
            field=models.EmailField(help_text='Please Provide Email Address ', max_length=254),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Facebook',
            field=models.URLField(help_text='Facebook Page URL'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='LinkedIn',
            field=models.URLField(help_text='LinkedIn Profile URL'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Patient_Image',
            field=models.ImageField(help_text='Informative Image Of Patient', upload_to='patient_images/'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Question1_Accept_Insurance_Policy',
            field=models.TextField(help_text='Please Answer The Question: Do You Accept Insurance Policy?', null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Question2_Is_Emergency_Unit_Available',
            field=models.TextField(help_text='Please Answer The Question:Is Emergency Unit Available?', null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Question3_Provide_Telehealth_Health',
            field=models.TextField(help_text='Please Answer The Question: Do You Provide Telehealth Service?', null=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='Youtube',
            field=models.URLField(help_text='Youtube Channel URL '),
        ),
        migrations.AlterField(
            model_name='sitepurchase',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
