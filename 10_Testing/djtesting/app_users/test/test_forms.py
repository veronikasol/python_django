from django.test import TestCase
from ..forms import RegisterForm, ProfileEditForm

# Тестирование приложения для учета пользователей
"""Пользователи могут 
	незарегистрированные - зарегистрироваться на сайте
	зарегистрированные:
		залогиниться на сайте
		смотреть свой профиль
		редактировать свой профиль
"""

class UserRegistrationFormTest(TestCase):
	"""Может ли пользователь зарегистрироваться на сайте указав имя и пароль:
	По адресу register 
	пользователь видит форму для регистрации
	Вводит свои данные 
	и при успешной регистрации перенаправляется на главную страницу 
	как аутентифицированный и залогиненный
	"""

	def test_proper_register_form(self):
		response = self.client.get('/user/register')
		self.assertIsInstance(response.context['form'], RegisterForm)

	def test_registration_form_renders(self):
		form_bad = RegisterForm(data={'username':'test', 'password':''})
		self.assertFalse(form_bad.is_valid())
		form_good = RegisterForm(data={'username':'test_1', 'password1':'secret_1A', 'password2':'secret_1A'})
		self.assertTrue(form_good.is_valid())


class ProfileEditFormTest(TestCase):
	"""Может ли пользователь изменить данные профиля
	По адресу /user/edit/user_id 
	пользователь видит форму для редактирования профиля
	Вводит свои данные 
	если успешно перенаправляется на страницу профиля
	"""

	def test_proper_register_form(self):
		response = self.client.get('/user/register')
		self.assertIsInstance(response.context['form'], RegisterForm)

	def test_registration_form_renders(self):
		form_bad = RegisterForm(data={'username':'test', 'password':''})
		self.assertFalse(form_bad.is_valid())
		form_good = RegisterForm(data={'username':'test_1', 'password1':'secret_1A', 'password2':'secret_1A'})
		self.assertTrue(form_good.is_valid())

