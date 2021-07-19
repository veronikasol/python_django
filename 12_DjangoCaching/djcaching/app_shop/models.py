from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True, verbose_name=_('category'))
	ru_name = models.CharField(max_length=200, blank =True, default='', verbose_name=_('category_ru'))
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _('category')
		verbose_name_plural = _('categories')
	
	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=200, db_index=True, verbose_name=_('product'))
	ru_name = models.CharField(max_length=200, blank =True, default='', verbose_name=_('product_ru'))
	description = models.TextField(blank=True, default='')
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	image = models.FileField(upload_to='products/', blank=True, verbose_name=_('image'))
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
	available = models.BooleanField(default=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _('product')
		verbose_name_plural = _('products')
	
	def __str__(self):
		return self.name


class OrderItem(models.Model):
	user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))

	def __str__(self):
		return f'{self.product} for {self.user.username} quantity {self.quantity}'

	def get_cost(self):
		return self.price*self.quantity


class Offer(models.Model):
	name = models.CharField(max_length=200, db_index=True, verbose_name=_('offer'))
	ru_name = models.CharField(max_length=200, blank =True, default='', verbose_name=_('ru_offer'))
	product = models.ManyToManyField(Product)
	discount = models.IntegerField()
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Promo(models.Model):
	name = models.CharField(max_length=200, db_index=True, verbose_name=_('promo'))
	ru_name = models.CharField(max_length=200, blank =True, default='', verbose_name=_('ru_promo'))
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	discount = models.IntegerField()
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class UserAccount(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=300, verbose_name=_('balance'))
	promo = models.ManyToManyField(Promo)
	offer = models.ManyToManyField(Offer)

	def __str__(self):
		return self.user.username


