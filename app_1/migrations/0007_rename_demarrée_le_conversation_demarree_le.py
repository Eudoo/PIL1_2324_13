# Generated by Django 5.0.6 on 2024-06-14 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0006_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='demarrée_le',
            new_name='demarree_le',
        ),
    ]
