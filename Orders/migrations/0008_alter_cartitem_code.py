# Generated by Django 4.0 on 2023-11-27 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0007_alter_cartitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='code',
            field=models.CharField(default='', max_length=10),
        ),
    ]