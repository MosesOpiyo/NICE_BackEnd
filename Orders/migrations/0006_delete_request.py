# Generated by Django 4.0 on 2023-09-30 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0005_rename_is_accepted_request_is_approved_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Request',
        ),
    ]
