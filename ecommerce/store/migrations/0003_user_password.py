# Generated by Django 5.1.3 on 2024-11-19 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_user_remove_userprofile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]