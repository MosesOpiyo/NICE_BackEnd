# Generated by Django 4.0 on 2023-09-04 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0001_initial'),
        ('Farming', '0002_coffeeproducts_acidity_coffeeproducts_caffeine_and_more'),
        ('Warehouser', '__first__'),
        ('Orders', '0002_order_country_order_date_order_marker_order_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_warehoused', models.BooleanField(default=False)),
                ('producer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Authentication.farmer')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Farming.coffeeproducts')),
                ('warehouse', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Warehouser.warehouse')),
            ],
        ),
    ]