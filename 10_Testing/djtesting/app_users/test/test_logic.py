from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..forms import RegisterForm

# Тестирование приложения для учета пользователей
"""Пользователи могут 
	незарегистрированные - зарегистрироваться на сайте
	зарегистрированные:
		залогиниться на сайте
		смотреть свой профиль
		редактировать свой профиль
"""

class UserRegistrationLogicTest(TestCase):
	"""Может ли пользователь зарегистрироваться на сайте указав имя и пароль:
	По адресу register 
	пользователь видит форму для регистрации
	Вводит свои данные 
	и при успешной регистрации перенаправляется на главную страницу 
	как аутентифицированный и залогиненный
	"""

	def test_user_created_after_post_request(self):

		response = self.client.post('/user/register', data={
			'username':'test_3', 
			'password1':'secret_1A', 
			'password2':'secret_1A'
			}, follow=False, secure=True)
		self.assertEqual(response.status_code, 302)
		self.assertIn(User.objects.first().username,'test_3')
		