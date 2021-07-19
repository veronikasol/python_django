from django.test import TestCase
from ..models import Category, Product, OrderItem, Offer, Promo, UserAccount
from django.contrib.auth.models import User
import random

# Тестирование приложения кабинета лояльности
""" Корректность создания моделей:
	Категория товара - Category
	Товар - Product
	Пункт в заказе - OrderItem
	Предложения - Offer
	Скидки Promo
	Личный кабинет пользователя - UserAccount
"""

class UseraccountCreationModelTest(TestCase):
	"""Корректно ли создается данные для личного кабинета
	"""

	def test_can_create_user_account(self):
		user = User.objects.create(username='test_model')
		categ_names = ['cake','pancake', 'cookie']
		for i in range(3):
			Category.objects.create(name=categ_names[i], slug=categ_names[i])
		prod_names = ['strawberry', 'coconut', 'cherry']
		categories = Category.objects.all()
		for i in range(3):
			Product.objects.create(
				name=f'{prod_names[i]} {categ_names[i]}',
				category=categories[i], price=random.randint(10,40))
		products = Product.objects.all()
		times = ['summer','autumn', 'winter', 'spring']
		ru_times = ['Лето','Осень', 'Зима', 'Весна']
		for i in range(5):
			time_idx = random.randint(0,3)
			time = times[time_idx]
			ru_time = ru_times[time_idx]
			desc = random.randint(10,90)
			product = products[random.randint(0,len(products)-1)]
			name = f'{time} discount {desc}% for {product.name}'
			ru_name = f'{ru_time} скидка {desc}% на {product.ru_name}'
			of = Offer.objects.create(name=name, ru_name=ru_name, discount=desc)
			of.product.add(product)
		account = UserAccount.objects.create(user=user)
		offers = Offer.objects.all()
		for of in offers:
			account.offer.add(of)
		self.assertTrue(User.objects.all().filter(id=1))
		self.assertIn(User.objects.first().username,'test_model')
		self.assertTrue(UserAccount.objects.all().filter(id=1))
		self.assertIn(User.objects.first().username,'test_model')
		self.assertIn(Category.objects.first().name,'cake')
		self.assertTrue(Product.objects.all().filter(id=1))
		self.assertTrue(Offer.objects.all().filter(id=3))