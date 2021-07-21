from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Category, Product, UserAccount, Promo, Offer, OrderItem
from django.core.cache import cache
from django.views import View


class MainView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'main.html')


def product_list(request, category_slug=None, *args, **kwargs,):
	category = None
	translate = False
	language = request.LANGUAGE_CODE
	if language == 'ru':
		translate = True
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	context = {'category':category,
		'categories':categories,
		'products':products,
		'translate': translate}
	return render(request, 'app_shop/product/list.html', context=context)

def product_detail(request, pk, *args, **kwargs):
	product = get_object_or_404(Product, id=pk, available=True)
	translate = False
	language = request.LANGUAGE_CODE
	if language == 'ru':
		translate = True
	context = {'product':product, 'translate': translate}
	return render(request, 'app_shop/product/detail.html', context=context)

def user_account(request, user_id, *args, **kwargs):
	user = User.objects.get(pk=user_id)
	translate = False
	if user != request.user:
		return HttpResponse('You cannot view another people account!')
	if UserAccount.objects.filter(user=user).exists():
		user_account = UserAccount.objects.get(user=user)
	else:
		user_account = UserAccount.objects.create(user=user)
		translate = False
	language = request.LANGUAGE_CODE
	if language == 'ru':
		translate = True
	promotions = user_account.promo.all()
	balance = user_account.balance
	#кеширование
	history_cache_key = f'hystory:{user.username}'
	offers_cache_key = f'offers:{user.username}'
	offers = cache.get(offers_cache_key)
	if not offers:
		offers = user_account.offer.all().filter(ru_name__icontains='торт')
		cache.set(offers_cache_key,offers, 10*60)
	payment_history = cache.get(history_cache_key)
	if not payment_history:
		payment_history = get_history(user) # products, ru_products, total_sum
		cache.set(history_cache_key,payment_history, 10*60)
	context = {'promotions':promotions, 
		'offers':offers, 
		'balance':balance,
		'payment_history':payment_history,
		'translate': translate
		}
	return render(request, 'app_shop/account/account.html', context=context)


def get_history(user):
	payment_history = OrderItem.objects.filter(user=user)
	total_sum = 0
	for prod in payment_history:
		total_sum += prod.price * prod.quantity
	products = list(set([payment_history[i].product.name for i in range(len(payment_history))]))
	ru_products = list(set([payment_history[i].product.ru_name for i in range(len(payment_history))]))
	return {'products':products, 'ru_products':ru_products, 'total_sum':total_sum}