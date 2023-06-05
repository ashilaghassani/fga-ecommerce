from django.db import models


PILIHAN_LABEL = [
    ('Expensive', 'Diatas 20 juta'),
    ('Middle', 'Antara 1-20 juta'),
    ('Cheap', 'Dibawah 1 juta')
]


PILIHAN_KATEGORI = [
    ('Expensive', 'Yang berhubungan dengan fashion'),
    ('Gadget', 'Yang berhubungan dengan gadget'),
    ('Food', 'Yang berhubungan dengan makanan')
]

# Create your models here.
class ProductItem(models.Model):
    nama_produk = models.CharField(max_length=100)
    harga = models.FloatField()
    harga_diskon = models.FloatField(blank=True , null=True)
    slug = models.SlugField(unique=True)
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='product_pics')
    label = models.CharField(choices=PILIHAN_LABEL,max_length=9)
    kategori = models.CharField(choices=PILIHAN_KATEGORI,max_length=9)
