from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..forms import PostForm, MultiFileForm

class PostFormTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='test_12')
		self.user.set_password('secret_12A')
		self.user.save()
		self.client.login(username='test_12', password='secret_12A')


	def test_proper_post_form(self):
		response = self.client.get('/posts/')
		self.assertIsInstance(response.context['post_form'], PostForm)
		self.assertIsInstance(response.context['file_form'], MultiFileForm)

	def test_post_form_renders(self):
		form_bad = PostForm(data={})
		self.assertFalse(form_bad.is_valid())
		form_good = PostForm(data={'title':'test_1', 'content':'secret_1A'})
		file_good = MultiFileForm(data={'file':'kjdfkjdkfdkf.jdk'})
		self.assertTrue(form_good.is_valid())
		self.assertTrue(file_good.is_valid())