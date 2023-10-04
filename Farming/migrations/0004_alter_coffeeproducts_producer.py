# Generated by Django 4.0 on 2023-09-15 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_account_index'),
        ('Farming', '0003_coffeeproducts_requested_warehousing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffeeproducts',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.account'),
        ),
    ]
