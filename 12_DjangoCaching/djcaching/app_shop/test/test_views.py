from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..views import product_list, product_detail, user_account

class UserAccountViewTest(TestCase):
	
	def setUp(self):
		self.credentials = {'username':'test_13', 'password':'secret_13A'}
		self.user = User.objects.create_user(username='test_13')
		self.user.set_password('secret_13A')
		self.user.save()
		self.client.login(username='test_13', password='secret_13A')

	
	def test_can_see_user_account_detail(self):
		response = self.client.get(f'/app_shop/account/{self.user.id}')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, user_account)
		self.assertTemplateUsed(response, 'app_shop/account/account.html')
		self.assertIn('balanse', response.content.decode())


class ProductListViewTest(TestCase):

	def test_can_see_product_list(self):
		response = self.client.get('/app_shop/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.resolver_match.func, product_list)
		self.assertTemplateUsed(response, 'app_shop/product/list.html')
		self.assertContains(response, 'sweet shop')
