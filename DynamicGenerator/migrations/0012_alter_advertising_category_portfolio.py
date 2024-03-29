# Generated by Django 5.0.2 on 2024-03-22 20:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0011_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertising',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to='DynamicGenerator.category'),
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255, null=True)),
                ('Profile_Image', models.ImageField(upload_to='Portfolio/')),
                ('Logo', models.ImageField(upload_to='logos/')),
                ('Profession', models.CharField(max_length=255, null=True)),
                ('Skill', models.CharField(max_length=255, null=True)),
                ('Short_Intro', models.TextField()),
                ('About_Profession', models.CharField(max_length=255, null=True)),
                ('Cover_Image', models.ImageField(upload_to='CoverImage/')),
                ('First_Service', models.CharField(help_text='First Service Name', max_length=255)),
                ('First_Service_Description', models.TextField(help_text='First Service Description')),
                ('Second_Service', models.CharField(help_text='Second Service Name', max_length=255)),
                ('Second_Service_Description', models.TextField(help_text='Second Service Description')),
                ('Third_Service', models.CharField(help_text='Third Service Description', max_length=255)),
                ('Third_Service_Description', models.TextField(help_text='Third Service Name')),
                ('Foutrth_Service', models.CharField(help_text='Fourth Service Name(optional)', max_length=255)),
                ('Fourth_Service_Description', models.TextField(help_text='Fourth Service Description(optional)')),
                ('First_Project_Name', models.CharField(max_length=255)),
                ('First_Project_Description', models.TextField()),
                ('First_Project_Image', models.ImageField(upload_to='ProjectImage/')),
                ('First_Project_Url', models.URLField()),
                ('First_Project_Skill_OR_Framework_Use', models.CharField(max_length=255)),
                ('Second_Project_Name', models.CharField(max_length=255)),
                ('Second_Project_Description', models.TextField()),
                ('Second_Project_Image', models.ImageField(upload_to='ProjectImage/')),
                ('Second_Project_Url', models.URLField()),
                ('Second_Project_Skill_OR_Framework_Use', models.CharField(max_length=255)),
                ('Third_Project_Name', models.CharField(max_length=255)),
                ('Third_Project_Description', models.TextField()),
                ('Third_Project_Image', models.ImageField(upload_to='ProjectImage/')),
                ('Third_Project_Url', models.URLField()),
                ('Third_Project_Skill_OR_Framework_Use', models.CharField(max_length=255)),
                ('Total_Number_Of_Projects', models.IntegerField(default=0)),
                ('Total_Clients', models.IntegerField(default=0)),
                ('Experience', models.IntegerField(default=0)),
                ('Awards', models.IntegerField(default=0)),
                ('First_Client_Quote', models.TextField()),
                ('First_Client_Position', models.CharField(max_length=255)),
                ('First_Clent_Image', models.ImageField(upload_to='ClientImage/')),
                ('Second_Client_Quote', models.TextField()),
                ('First_Client_Name', models.CharField(max_length=255)),
                ('Second_Client_Position', models.CharField(max_length=255)),
                ('Second_Clent_Image', models.ImageField(upload_to='ClientImage/')),
                ('Third_Client_Quote', models.TextField()),
                ('Third_Client_Name', models.CharField(max_length=255)),
                ('Third_Client_Position', models.CharField(max_length=255)),
                ('Third_Clent_Image', models.ImageField(upload_to='ClientImage/')),
                ('Whats_App_Number', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('Contact_Description', models.CharField(max_length=255)),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('youtube_link', models.URLField(blank=True, null=True)),
                ('instagram_link', models.URLField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
