# Generated by Django 4.0 on 2024-02-11 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0014_cartitem_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='weight',
            field=models.CharField(default='', max_length=100, null=True),
        ),
    ]
