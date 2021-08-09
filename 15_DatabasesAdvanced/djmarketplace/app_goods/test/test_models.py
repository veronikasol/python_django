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
				category=categories[i])
		products = Product.objects.all()
		account = UserAccount.objects.create(user=user)

		self.assertTrue(User.objects.all().filter(id=1))
		self.assertIn(User.objects.first().username,'test_model')
		self.assertTrue(UserAccount.objects.all().filter(id=1))
		self.assertIn(User.objects.first().username,'test_model')
		self.assertIn(Category.objects.first().name,'cake')
		self.assertTrue(Product.objects.all().filter(id=1))