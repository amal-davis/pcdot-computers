# Generated by Django 4.2.5 on 2024-07-21 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcdotapp', '0009_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='delivery_charge',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
