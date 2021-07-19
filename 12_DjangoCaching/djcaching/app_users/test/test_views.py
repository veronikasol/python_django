from django.test import TestCase
from django.urls import reverse
from ..views import register_view, profile_view, profile_edit_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from ..models import Profile
from django.contrib.auth import authenticate


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
		response = self.client.get('/app_users/register')
		self.assertEqual(response.resolver_match.func, register_view)
		self.assertTemplateUsed(response, 'app_users/register.html')
		self.assertEqual(response.status_code, 200)
		

class UserLoginViewTest(TestCase):
	"""Зарегистрированный пользователь может 
		залогиниться по адресу login 
	"""

	def test_registered_user_login_view(self):
		response = self.client.get('/app_users/login/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func.__name__, auth_views.LoginView.as_view().__name__)
		self.assertTemplateUsed(response, 'registration/login.html')

class UserProfileViewTest(TestCase):
	"""Зарегистрированный пользователь может  
		посмотреть свой профиль по адресу <int:user_id>
		изменить свой профиль по адресу edit/<int:user_id>
		Вводит свои данные 
		если успешно перенаправляется на страницу профиля
	"""
	def setUp(self):
		self.credentials = {'username':'test_6', 'password':'secret_6A'}
		self.user = User.objects.create_user(username='test_6')
		self.user.set_password('secret_6A')
		self.user.save()
		self.profile = Profile.objects.create(user=self.user, date_of_birth=None,
				city='default', photo='anonymous.png')
		self.client.login(username='test_6', password='secret_6A')

	def test_can_see_user_profile(self):
		response = self.client.get(f'/app_users/{self.user.pk}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, profile_view)
		self.assertTemplateUsed(response, 'app_users/profile.html')
		self.assertIn(f'{self.profile.user.username}', response.content.decode())

	def test_loginned_user_can_see_another_user_profile(self):
		"""Создание другого пользователя(9) и получение его странички (не залогиненного(6))"""
		another_user = User.objects.create_user(username='test_9')
		another_user.set_password('secret_9A')
		another_user.save()
		another_profile = Profile.objects.create(user=another_user, date_of_birth=None,
				city='default', photo='anonymous.png')
		response = self.client.get(f'/app_users/{another_user.pk}')
		self.assertEqual(response.status_code, 200)
		self.assertIn(f'{another_profile.user.username}', response.content.decode())

	def test_can_see_user_edit_profile(self):
		response = self.client.get(f'/app_users/edit/{self.user.pk}' )
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, profile_edit_view)
		self.assertTemplateUsed(response, 'app_users/profile_edit.html')
		self.assertIn(f'{self.user.username}', response.content.decode())

	def test_can_change_profile(self):
		response = self.client.post(f'/app_users/edit/{self.user.pk}', data={
			'city':'not_default',
			'first_name': 'test_first_name', 
			'last_name': 'test_last_name'})
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response,f'/app_users/{self.user.pk}')
		self.profile.refresh_from_db()
		self.user.refresh_from_db()
		self.assertEqual(self.profile.city,'not_default')
		self.assertEqual(self.user.first_name,'test_first_name')
		self.assertEqual(self.user.last_name,'test_last_name')
		self.assertEqual(self.profile.photo,'anonymous.png')
