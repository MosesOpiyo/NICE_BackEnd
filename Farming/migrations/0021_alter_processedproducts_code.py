# Generated by Django 4.0 on 2023-11-27 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farming', '0020_processedproducts_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processedproducts',
            name='code',
            field=models.CharField(default='', max_length=10),
        ),
    ]