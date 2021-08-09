from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app_goods.models import Product, Shop, Content
from .app_cart import Cart 
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id, shop_id):
	cart = Cart(request)
	product = get_object_or_404(Product, pk=product_id)
	shop = get_object_or_404(Shop, pk=shop_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(
			product=product,
			shop=shop,
			quantity=cd['quantity'],
			update_quantity=cd['update']
			)
	return redirect('cart_detail')

def cart_remove(request, product_id, shop_id):
	cart = Cart(request)
	product = get_object_or_404(Product, pk=product_id)
	shop = get_object_or_404(Shop, pk=shop_id)
	cart.remove(product, shop)
	return redirect('cart_detail')

def cart_detail(request, *args, **kwargs):
	translate = False
	language = request.LANGUAGE_CODE
	if language == 'ru':
		translate = True
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(
			initial={'quantity':item['quantity'], 'update': True})
	return render(request, 'app_cart/detail.html', {'cart': cart, 'translate': translate})