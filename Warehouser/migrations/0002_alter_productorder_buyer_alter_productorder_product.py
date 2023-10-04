# Generated by Django 4.0 on 2023-10-02 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0012_originwarehouser_alter_account_type'),
        ('Farming', '0007_coffeeproducts_shipment_successful'),
        ('Warehouser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='buyer',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='Authentication.buyer'),
        ),
        migrations.AlterField(
            model_name='productorder',
            name='product',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='Farming.processedproducts'),
        ),
    ]
