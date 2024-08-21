# Generated by Django 4.2.5 on 2024-07-21 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcdotapp', '0010_product_delivery_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_charge',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]