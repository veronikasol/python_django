from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..views import posts_view, post_detail, PostCreateView
from ..models import Post

"""
Сценарий.
Незарегистрированный пользователь может
	открывает главную страницу по адресу '/'
	видит приглашение войти или зарегистрироваться
	видит список постов
	список постов упорядочен по дате по убыванию (сначала новые)
	для каждой записи отображается 100 символов текста и автор
	можно перейти на детальное отображение записи
	На страничке с деталями публикации:
		текст
		файлы прикрепленные
Незарегистрированный пользователь не может
	публиковать записи 
Зарегистрированный пользователь может с главной страницы по адресу '/' перейти по ссылкам:
	выйти - и он будет разлогинен, 
	добавить запись, загрузить файл с несколькими записями,
	просмотреть свой профиль, редактировать свой профиль
Зарегистрированный пользователь
	публикует запись и она отражается в списке публикаций и ее можно посмотреть детально
	при прикреплении файлов, файлы тоже отображаются в детальном виде;
	загружает файл с несколькими записями и они отображаются в списке,
"""

class AnonymousBlogActionsTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='test_15')
		self.user.set_password('secret_15A')
		self.user.save()
		self.factory = RequestFactory()

	def test_anonymous_user_can_see_main_page(self):
		request = self.factory.get('/')
		request.user = AnonymousUser()
		response = posts_view(request)
		self.assertEqual(response.status_code, 200)
		self.assertIn('Новые публикации', response.content.decode())
		self.assertIn('Войти', response.content.decode())
		self.assertIn('Зарегистрироваться', response.content.decode())

	def test_anonymous_can_see_publications(self):
		post_1 = Post.objects.create(
			title='Test publication 1', 
			content='Nothing more but test 1.',
			user=self.user)
		post_2 = Post.objects.create(
			title='Test publication 2', 
			content='Nothing more but test 2.',
			user=self.user)
		post_3 = Post.objects.create(
			title='Test publication 3', 
			content='Nothing more but test 3.',
			user=self.user)
		request = self.factory.get('/')
		request.user = AnonymousUser()
		response = posts_view(request)
		self.assertIn(self.user.username, response.content.decode())
		self.assertIn('Test publication 2', response.content.decode())
		response = self.client.get(f'/{post_2.pk}')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Nothing more but test 2.',response.content.decode())


	def test_anonymous_user_cannot_post_publications(self):
		request = self.factory.post('/posts/', data={
			'title':'test_1', 
			'content':'secret_1A',
			})
		request.user = AnonymousUser()
		view = PostCreateView()
		view.setup(request)
		response = view.post(request)
		self.assertFalse(Post.objects.all())
		self.assertEqual(response.status_code, 200)
		self.assertIn('You are noa allowed to create posts', response.content.decode())
