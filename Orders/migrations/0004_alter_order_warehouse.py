# Generated by Django 4.0 on 2023-11-27 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Warehouser', '0002_alter_shippingmanifest_number'),
        ('Orders', '0003_alter_order_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Warehouser.warehouse'),
        ),
    ]
