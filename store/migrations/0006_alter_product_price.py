# Generated by Django 4.2.1 on 2023-06-04 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_deskripsi_product_tahun'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
