from django.db import models
from product_item.models import ProductItem

# Create your models here.
class Order(models.Model):
    produk_items = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    tanggal_mulai = models.DateTimeField(auto_now_add=True)
    tanggal_order = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)