from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Category, Product, UserAccount, Promo, Offer, OrderItem
from django.core.cache import cache

def product_list(request, category_slug=None):
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
	offers = user_account.offer.all().filter(ru_name__icontains='торт')
	balance = user_account.balance
	payment_history = OrderItem.objects.filter(user=user)
	#кеширование
	offers_cache_key = f'offers:{user.username}'
	promo_cache_key = f'promo:{user.username}'
	cache.get_or_set(promo_cache_key,promotions, 30*60)
	cache.get_or_set(offers_cache_key,offers, 30*60)
	context = {'promotions':promotions, 
		'offers':offers, 
		'balance':balance,
		'payment_history':payment_history,
		'translate': translate
		}
	return render(request, 'app_shop/account/account.html', context=context)