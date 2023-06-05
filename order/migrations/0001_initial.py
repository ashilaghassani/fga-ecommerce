# Generated by Django 4.2 on 2023-05-29 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_mulai', models.DateTimeField(auto_now_add=True)),
                ('tanggal_order', models.DateTimeField(blank=True, null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('produk_items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_item.productitem')),
            ],
        ),
    ]