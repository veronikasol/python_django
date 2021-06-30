from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Post, File


class PostModelTest(TestCase):
	"""Корректно ли создается запись в списке постов
	"""
	def setUp(self):
		self.user = User.objects.create_user(username='test_11')
		self.user.set_password('secret_11A')
		self.user.save()
		self.client.login(username='test_11', password='secret_11A')

	def test_can_create_post(self):
		post = Post.objects.create(
			title='Test publication', 
			content='Nothing more but test.',
			user=self.user)
		self.assertTrue(Post.objects.all().filter(id=1))
		self.assertIn(Post.objects.first().user.username,'test_11')
		self.assertIn(Post.objects.first().title,'Test publication')
		self.assertTrue(Post.objects.all().filter(id=1))

	def test_can_attach_file_to_the_post(self):
		post = Post.objects.create(
			title='Test publication with file', 
			content='Nothing more but test with file.',
			user=self.user)
		file = File.objects.create(
			file='some_file',
			post=post)
		self.assertTrue(File.objects.all().filter(id=1))
		self.assertEqual(File.objects.first().post, post)