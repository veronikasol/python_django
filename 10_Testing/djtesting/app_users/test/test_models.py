from django.test import TestCase
from ..models import Profile
from django.contrib.auth.models import User

# Тестирование приложения для учета пользователей
"""Пользователи могут 
	незарегистрированные - зарегистрироваться на сайте
	зарегистрированные:
		залогиниться на сайте
		смотреть свой профиль
		редактировать свой профиль
"""

class UserRegistrationModelTest(TestCase):
	"""Корректно ли создается запись в профиле
	"""

	def test_can_create_user_during_registration(self):
		user = User.objects.create(username='test_model')
		Profile.objects.create(user=user)
		self.assertTrue(User.objects.all().filter(id=1))
		self.assertIn(User.objects.first().username,'test_model')
		self.assertTrue(Profile.objects.all().filter(id=1))