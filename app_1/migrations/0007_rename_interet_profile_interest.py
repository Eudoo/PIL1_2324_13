# Generated by Django 5.0.6 on 2024-06-12 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0006_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='interet',
            new_name='interest',
        ),
    ]
