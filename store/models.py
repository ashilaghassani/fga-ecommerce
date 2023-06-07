from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)

    def __str__(self):
        return self.name if self.name else ''

PILIHAN_LABEL = (
	('NEW','info'),
	('SALE','danger'),
	('BEST', 'primary'),
)

PILIHAN_KATEGORY = (
	('NV','Novel'),
	('CM','Comic'),
	('MG', 'Magazine'),
	('EC', 'Encyclopedia'),
)


class Product(models.Model):
	pid = models.IntegerField(null=True)
	name = models.CharField(max_length=200)
	author_name = models.CharField(max_length=100, null=True)
	tahun = models.IntegerField(null=True)
	deskripsi =  models.TextField(null=True)
	price = models.DecimalField(max_digits=30,decimal_places=2)
	discount_price = models.DecimalField(max_digits=30,decimal_places=2,null=True)
	image = models.ImageField(null=True, blank=True)
	label = models.CharField(choices=PILIHAN_LABEL,max_length=4,null=True)
	kategori = models.CharField(choices=PILIHAN_KATEGORY,max_length=2,null=True)
	digital = models.BooleanField(default=False,null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
	class Meta:
		ordering =['name']

class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.image.url
    

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = 0
		for item in orderitems:
			product = item.product
			if product.discount_price and product.discount_price != 0:
				total += product.discount_price * item.quantity
			else:
				total += product.price * item.quantity
		return total
 
	
	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
	
	@property
	def get_discount_amount(self):
		orderitems = self.orderitem_set.all()
		discount_amount = 0
		for item in orderitems:
			product = item.product
			if product.discount_price and product.discount_price != 0:
				discount_amount += (product.price - product.discount_price) * item.quantity
		return discount_amount
	
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping




class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	
	@property
	def get_total(self):
		total = 0
		if self.product.discount_price and self.product.discount_price != 0:
			total = self.product.discount_price * self.quantity
		else:
			total = self.product.price * self.quantity
		return total
	
	@property
	def get_discount_amount(self):
		if self.product.discount_price and self.product.discount_price != 0:
			discount_amount = (self.product.price - self.product.discount_price) * self.quantity
		else:
			discount_amount = 0
		return discount_amount
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
	

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    message = models.TextField(max_length=1200)
    def __str__(self):
        return self.email