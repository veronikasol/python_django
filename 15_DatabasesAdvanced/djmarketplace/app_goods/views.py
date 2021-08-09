from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Category, Product, UserAccount, Promo, Offer, OrderItem
from .models import Shop, Content, Order
from django.core.cache import cache
from django.views import View
from app_cart.forms import CartAddProductForm
from .forms import BalanceIncreaseForm
from app_cart.app_cart import Cart
from django.db import transaction
from decimal import Decimal
from django.db.models import Count


class MainView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'main.html')


def product_list(request, category_slug=None, shop_slug=None, *args, **kwargs,):
	category = None
	shop = None
	translate = False
	language = request.LANGUAGE_CODE
	if language == 'ru':
		translate = True
	shops = Shop.objects.all()
	categories = Category.objects.all()
	content = Content.objects.order_by('shop')
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		content = content.filter(product__category=category)
	if shop_slug:
		shop = get_object_or_404(Shop, slug=shop_slug)
		content = content.filter(shop=shop)
		shops = shops.filter(slug=shop_slug)
	nums = Product.objects.annotate(
		num_purchases=Count('order_items')).order_by('-num_purchases')[:5]
	context = {'category':category,
		'categories':categories,
		'shops':shops,
		'content':content,
		'translate': translate,
		'nums':nums}
	return render(request, 'app_goods/product/list.html', context=context)

def product_detail(request, pk, *args, **kwargs):
	item = get_object_or_404(Content, id=pk, available=True)
	product = get_object_or_404(Product, id=item.product.id)
	cart_product_form = CartAddProductForm()
	translate = False
	language = request.LANGUAGE_CODE
	if language == 'ru':
		translate = True
	context = {
		'item':item,
		'product':product,
		'translate': translate,
		'cart_product_form': cart_product_form
		}
	return render(request, 'app_goods/product/detail.html', context=context)

def user_account(request, *args, **kwargs):
	user = request.user
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
		status = get_status(payment_history['total_sum'])
		user_account.status = status
		user_account.save()
		cache.set(history_cache_key,payment_history, 1*60)
	status = user_account.get_status_display()
	context = {'promotions':promotions, 
		'offers':offers, 
		'balance':balance,
		'payment_history':payment_history,
		'status': status,
		'translate': translate
		}
	return render(request, 'app_goods/account/account.html', context=context)


def get_history(user):
	order_history = Order.objects.filter(user=user) # заказы
	order_items = OrderItem.objects.select_related('product').filter(order__in=order_history)
	all_products = []
	ru_all_products = []
	orders = [f'#{item.id}: {item.created.date()}' for item in order_history]
	total_spent = 0
	for item in order_items:
		all_products.append(item.product.name)
		ru_all_products.append(item.product.ru_name)
		total_spent += item.quantity * item.price
	return {
		'orders': orders,
		'products':set(all_products), 
		'ru_products':set(ru_all_products),
		'total_sum':total_spent}

def get_status(spent_sum):
	if spent_sum <= 100:
		return 'I'
	elif 100 < spent_sum <= 200:
		return 'S'
	elif 200 < spent_sum <= 300:
		return 'P'
	else:
		return 'G'


def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		user = request.user
		if user.is_authenticated:
			order = Order.objects.create(user=user)
			for item in cart:
				shop = Shop.objects.get(name=item['shop'])
				OrderItem.objects.create(order=order,
					product=item['product'],
					shop=shop,
					price=item['price'],
					quantity=item['quantity'])
			request.session['order_amount'] = str(cart.get_total_price())
			cart.clear()
			request.session['order_id'] = order.pk
			return redirect(reverse('payment_process'))
			#return render(request, 'app_goods/order/created.html', {'order':order})
		else:
			return HttpResponse('Please, log in to make purchases!')
	return render(request, 'app_goods/order/create.html', {'cart':cart})

def balance_increase(request, *args, **kwargs):
	if request.method == 'POST':
		user = request.user
		user_account = UserAccount.objects.get(user=user)
		form = BalanceIncreaseForm(request.POST)
		if form.is_valid():
			addition = form.cleaned_data['quantity']
			user_account.balance += addition
			user_account.save()
			return redirect(reverse('user_account'))
	else:
		form = BalanceIncreaseForm()
	return render(request, 'app_goods/account/balance_increase.html', {'form':form})

def payment_process(request):
	order_id = request.session.get('order_id')
	order = get_object_or_404(Order, pk=order_id)
	amount = request.session.get('order_amount')
	cart = Cart(request)
	if request.method == 'POST':
		#проверить, достаточный ли баланс
		if enough_money(request.user, amount):
			# atomic transactions
			with transaction.atomic():
				account = UserAccount.objects.get(user=request.user)
				account.balance -= Decimal(amount)
				account.save()
				order_items = OrderItem.objects.select_related('product').filter(order=order)
				for item in order_items:
					shop = Shop.objects.get(name=item.shop)
					product = Product.objects.get(name=item.product)
					quantity = item.quantity
					content = Content.objects.get(shop=shop, product=product)
					content.quantity -= quantity
					content.save()
				order.paid = True
				order.save()
				cart.clear()
				return redirect('payment_done')
		else:
			return redirect('payment_cancelled')
	return render(request, 'app_goods/payments/process.html', {'order': order, 'amount': amount})

def payment_done(request):
	return render(request, 'app_goods/payments/done.html')

def payment_canceled(request):
	return render(request, 'app_goods/payments/canceled.html')

def enough_money(user, ammount):
	account = UserAccount.objects.get(user=user)
	if account.balance < float(ammount):
		return False
	else:
		return True