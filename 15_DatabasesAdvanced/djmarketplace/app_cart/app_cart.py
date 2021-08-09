from decimal import Decimal
from django.conf import settings
from app_goods.models import Shop, Product, Content
from django.urls import reverse


class Cart(object):
	def __init__(self, request):
		"""Initialize cart object"""
		self.session = request.session # memorize current session
		cart = self.session.get(settings.CART_SESSION_ID) # try to get data from the cart
		if not cart:
			# if there's no cart make a new one as a dictionary
			# where key = product id, values = quantity and price
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, shop, quantity=1, update_quantity=False):
		"""Add product to the cart or update it's quantity """

		#double index by product and by shop
		product_id = str(product.pk) + '-' + str(shop.pk)
		stock = Content.objects.get(shop=shop, product=product)
		available_quantity = stock.quantity 
		if product_id not in self.cart:
			price = stock.price
			self.cart[product_id] = {
				'quantity': 0, 
				'shop': str(shop.name), 
				'price': str(price)
				}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		if self.cart[product_id]['quantity'] > available_quantity:
			self.cart[product_id]['quantity'] = available_quantity
		self.save()

	def save(self):
		self.session.modified = True

	def remove(self, product, shop):
		"""Remove item from the cart """
		product_id = str(product.pk) + '-' + str(shop.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		""" Iterates through the cart items """
		product_ids = self.cart.keys()
		product_ids = list(map(lambda x: x.split('-')[0], product_ids))
		products = Product.objects.filter(pk__in=product_ids)
		cart = self.cart.copy()
		for product in products:
			k = list(cart.keys())
			idx = [i for i in range(len(k)) if k[i].split('-')[0]== str(product.pk) ]
			for i in range(len(idx)):
				cart[k[idx[i]]]['product'] = product
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			item['shop'] = Shop.objects.get(name=item['shop'])
			yield item

	def __len__(self):
		""" Total nums of items in the cart """
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

	def clear(self):
		""" Clear the cart - remains it brand new """
		del self.session[settings.CART_SESSION_ID]
		self.save()