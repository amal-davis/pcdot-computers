# Generated by Django 4.2.5 on 2024-06-13 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcdotapp', '0006_desktopcarouselimage_mobilecarouselimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]