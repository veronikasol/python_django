from .models import Category, Product, UserAccount, Promo, Offer, OrderItem
from .models import Shop, Content, Order

def enough_money(user, ammount):
	account = UserAccount.objects.get(user=user)
	if account.balance < float(ammount):
		return False
	else:
		return True

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


def is_translate(request):
	language = request.LANGUAGE_CODE
	if language == 'ru':
		return True
	else:
		return False