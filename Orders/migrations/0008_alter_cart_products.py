# Generated by Django 4.0 on 2023-10-11 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farming', '0007_coffeeproducts_shipment_successful'),
        ('Orders', '0007_alter_cart_buyer_alter_order_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(to='Farming.ProcessedProducts'),
        ),
    ]