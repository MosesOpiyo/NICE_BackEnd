# Generated by Django 4.0 on 2023-12-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0019_alter_verificationcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode',
            name='code',
            field=models.CharField(default=0, max_length=5),
        ),
    ]
