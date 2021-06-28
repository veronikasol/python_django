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
	"""Может ли пользователь зарегистрироваться на сайте указав имя и пароль:
	По адресу register 
	пользователь видит форму для регистрации
	Вводит свои данные 
	и при успешной регистрации перенаправляется на главную страницу 
	как аутентифицированный и залогиненный
	"""

	def test_can_create_user_during_registration(self):
		response = self.client.get('/user/register')
		user = User.objects.create(username='test_model')
		Profile.objects.create(user=user)
		self.assertTrue(User.objects.all().filter(id=1))
		self.assertIn(User.objects.first().username,'test_model')