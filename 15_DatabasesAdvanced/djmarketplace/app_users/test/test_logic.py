from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Profile
from ..forms import RegisterForm
from ..views import profile_view, profile_edit_view
from django.conf import settings

# Тестирование приложения для учета пользователей
"""Пользователи могут 
	незарегистрированные - зарегистрироваться на сайте
	зарегистрированные:
		залогиниться на сайте
		смотреть свой профиль и профиль других
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

		response = self.client.post('/app_users/register', data={
			'username':'test_3', 
			'password1':'secret_1A', 
			'password2':'secret_1A'
			}, follow=False, secure=True)
		self.assertEqual(response.status_code, 302)
		self.assertIn(User.objects.first().username,'test_3')
		#self.assertRedirects(response,'/')

class UserLoginLogicTest(TestCase):
	"""так как для входа используется готовый вид и форма, 
	проверяю только логику
	Зарегистрированный пользователь может 
		залогиниться по адресу login 
		посмотреть свой профиль по адресу <int:user_id> (проверяю в test_views)
		изменить свой профиль по адресу edit/<int:user_id> (проверяю в test_views)
		не может менять профили других пользователей
	"""
	def setUp(self):
		self.credentials = {'username':'test_5', 'password':'secret_5A'}
		self.user = User.objects.create_user(username='test_5')
		self.user.set_password('secret_5A')
		self.user.save()
		self.profile = Profile.objects.create(user=self.user, date_of_birth=None,
				city='default', photo='anonymous.png')

	def test_registered_user_can_login(self):
		response = self.client.post(reverse('login'), data={
			'username':'test_5',
			'password':'secret_5A'
			}, follow=True, secure=True)
		self.assertRedirects(response,'/')
		
	def test_unregistered_user_cannot_login(self):
		response = self.client.post(reverse('login'), data={
			'username':'test_5',
			'password':'wrong_password'
			}, follow=True, secure=True)
		self.assertIn('Password doesn\'t', response.content.decode())

	def test_registered_user_cannot_edit_another_user_profile(self):
		login = self.client.login(username='test_5', password='secret_5A')
		self.assertTrue(login)
		another_user = User.objects.create_user(username='test_8')
		another_user.set_password('secret_8A')
		another_user.save()
		another_profile = Profile.objects.create(user=another_user, date_of_birth=None,
				city='default', photo='anonymous.png')
		response = self.client.post(f'/app_users/edit/{another_user.pk}', data={
			'city':'not_default',
			'first_name': 'test_first_name', 
			'last_name': 'test_last_name',})
		self.assertEqual(response.status_code, 200)
		self.assertIn('You cannot modify another people',response.content.decode())
		another_profile.refresh_from_db()
		another_user.refresh_from_db()
		self.assertNotEqual(another_profile.city,'not_default')
		self.assertNotEqual(another_user.first_name,'test_first_name')
		self.assertNotEqual(another_user.last_name,'test_last_name')

class AnonymousUserActionsTest(TestCase):
	"""Анонимный пользователь может просматривать профили пользователей, но не может их изменять"""
	def setUp(self):
		self.user = User.objects.create_user(username='test_10')
		self.user.set_password('secret_10A')
		self.user.save()
		self.profile = Profile.objects.create(user=self.user, date_of_birth=None,
				city='default', photo='anonymous.png')
		self.factory = RequestFactory()

	def test_anonymous_user_cannot_modify_user_profile(self):
		request = self.factory.get(f'/app_users/edit/{self.user.pk}')
		request.user = AnonymousUser()
		response = profile_edit_view(request,self.user.pk)
		self.assertEqual(response.status_code, 200)
		self.assertIn('You cannot modify another people', response.content.decode())