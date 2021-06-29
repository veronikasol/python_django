from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..views import PostCreateView
from ..models import Post

class PostCreationViewTest(TestCase):
	
	def setUp(self):
		self.credentials = {'username':'test_13', 'password':'secret_13A'}
		self.user = User.objects.create_user(username='test_13')
		self.user.set_password('secret_13A')
		self.user.save()
		self.client.login(username='test_13', password='secret_13A')

	def test_can_see_post_creation_form(self):
		response = self.client.get('/posts/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func.__name__, PostCreateView.as_view().__name__)
		self.assertTemplateUsed(response, 'app_blog/post_form.html')
		self.assertContains(response, 'Добавить публикацию')

	def test_can_post_publication(self):
		response = self.client.post('/posts/', data={
			'title':'test_1', 
			'content':'secret_1A',
			})
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response,'/')
		self.assertIn(Post.objects.first().user.username,'test_13')
		self.assertIn(Post.objects.first().title,'test_1')
		self.assertTrue(Post.objects.all().filter(id=1))

	def test_can_see_posted_publication_in_the_list(self):
		response = self.client.post('/posts/', data={
			'title':'test_1', 
			'content':'secret_1A',
			}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(response.content.decode(),'test_1')

	def test_can_see_posted_publication_in_detail(self):
		pass