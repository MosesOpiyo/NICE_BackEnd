# Generated by Django 4.0 on 2023-11-27 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0015_account_notifications'),
        ('Orders', '0002_remove_order_product_order_green_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.buyer'),
        ),
    ]
