from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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
from .utils import enough_money, get_history, get_status, is_translate


class MainView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'main.html')


def product_list(request, category_slug=None, shop_slug=None, *args, **kwargs,):
	category = None
	shop = None
	translate = is_translate(request)
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
	translate = is_translate(request)
	context = {
		'item':item,
		'product':product,
		'translate': translate,
		'cart_product_form': cart_product_form
		}
	return render(request, 'app_goods/product/detail.html', context=context)

@login_required
def user_account(request, *args, **kwargs):
	user = request.user
	if UserAccount.objects.filter(user=user).exists():
		user_account = UserAccount.objects.get(user=user)
	else:
		user_account = UserAccount.objects.create(user=user)
	translate = is_translate(request)
	balance = user_account.balance
	#кеширование истории
	history_cache_key = f'hystory:{user.username}'
	payment_history = cache.get(history_cache_key)
	if not payment_history:
		payment_history = get_history(user) # orders, products, ru_products, total_sum
		cache.set(history_cache_key,payment_history, 1*60)
	# получение статуса
	status = get_status(payment_history['total_sum'])
	user_account.status = status
	user_account.save()
	status = user_account.get_status_display()
	
	context = { 
		'balance':balance,
		'payment_history':payment_history,
		'status': status,
		'translate': translate
		}
	return render(request, 'app_goods/account/account.html', context=context)

@login_required
def order_create(request):
	cart = Cart(request)
	translate = is_translate(request)
	if request.method == 'POST':
		user = request.user
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
	return render(request, 'app_goods/order/create.html', {'cart':cart, 'translate':translate})

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
			return redirect('payment_canceled')
	return render(request, 'app_goods/payments/process.html', {'order': order, 'amount': amount})

def payment_done(request):
	return render(request, 'app_goods/payments/done.html')

def payment_canceled(request):
	return render(request, 'app_goods/payments/canceled.html')