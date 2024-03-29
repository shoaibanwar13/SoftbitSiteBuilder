# Generated by Django 5.0.2 on 2024-03-21 18:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DynamicGenerator', '0010_advertising_short_about_us2'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=5)),
                ('profession', models.CharField(max_length=200, null=True)),
                ('bio', models.TextField(null=True)),
                ('profilepic', models.ImageField(null=True, upload_to='profilepic/')),
                ('created', models.DateTimeField(auto_now=True)),
                ('balance', models.IntegerField(default=0)),
                ('withdrawl_amount', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
                ('recommended_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
