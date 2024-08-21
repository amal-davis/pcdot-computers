# Generated by Django 4.2.5 on 2024-08-11 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcdotapp', '0011_order_delivery_charge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('name_en', models.CharField(max_length=255, null=True, verbose_name='name')),
                ('name_ar', models.CharField(max_length=255, null=True, verbose_name='name')),
                ('website', models.URLField(blank=True, null=True)),
            ],
        ),
    ]