# Generated by Django 4.0 on 2023-11-28 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0015_account_notifications'),
        ('Warehouser', '0002_alter_shippingmanifest_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='warehouser',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Authentication.account'),
        ),
    ]
