from django.test import TestCase
from django.urls import reverse
from ..views import register_view, profile_view, profile_edit_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from ..models import Profile


# Тестирование приложения для учета пользователей
"""Пользователи могут 
	незарегистрированные - зарегистрироваться на сайте
	зарегистрированные:
		залогиниться на сайте
		смотреть свой профиль
		редактировать свой профиль
"""

class UserRegistrationTest(TestCase):
	"""Может ли пользователь зарегистрироваться на сайте указав имя и пароль:
	По адресу register 
	пользователь видит форму для регистрации
	Вводит свои данные 
	и при успешной регистрации перенаправляется на главную страницу 
	как аутентифицированный и залогиненный
	"""

	def test_proper_register_view(self):
		response = self.client.get('/user/register')
		self.assertEqual(response.resolver_match.func, register_view)
		self.assertTemplateUsed(response, 'app_users/register.html')
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Регистрация')


class UserLoginViewTest(TestCase):
	"""Зарегистрированный пользователь может 
		залогиниться по адресу login 
	"""

	def test_registered_user_login_view(self):
		response = self.client.get('/user/login/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func.__name__, auth_views.LoginView.as_view().__name__)
		self.assertTemplateUsed(response, 'registration/login.html')
		self.assertContains(response, 'Введите логин и пароль')

class UserProfileViewTest(TestCase):
	"""Зарегистрированный пользователь может  
		посмотреть свой профиль по адресу <int:user_id>
		изменить свой профиль по адресу edit/<int:user_id>
	"""
	def setUp(self):
		self.credentials = {'username':'test_6', 'password':'secret_6A'}
		self.user = User.objects.create_user(**self.credentials)
		self.profile = Profile.objects.create(user=self.user, date_of_birth=None,
				city='default', photo='anonymous.png')

	def test_can_see_user_profile(self):
		response = self.client.get(f'/user/{self.user.pk}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, profile_view)
		self.assertTemplateUsed(response, 'app_users/profile.html')
		self.assertContains(response, 'Учетная запись пользователя')
		self.assertIn(f'{self.profile.user.username}', response.content.decode())

	def test_can_see_user__edit_profile(self):
		self.client.login(**self.credentials)
		response = self.client.get(f'/user/edit/{self.user.pk}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, profile_edit_view)
		self.assertTemplateUsed(response, 'app_users/profile_edit.html')
		self.assertContains(response, 'Редактрирование учетной записи пользователя')
		#self.assertIn(f'{self.profile.user.username}', response.content.decode())