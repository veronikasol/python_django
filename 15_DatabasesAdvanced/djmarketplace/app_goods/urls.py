from django.urls import path
from .views import MainView
from .views import product_list, product_detail, user_account
from .views import order_create, balance_increase
from .views import payment_process, payment_done, payment_canceled

urlpatterns = [
	path('', MainView.as_view(), name='main'),
	path('products/', product_list, name='product_list'),
	path('products/detail/<int:pk>/', product_detail, name='product_detail'),
	path('products/<slug:category_slug>/', product_list, name='product_list_by_category'),
	path('shop/<slug:shop_slug>/', product_list, name='product_list_by_shop'),
	path('account/', user_account, name='user_account'),
	path('order/create/', order_create, name='order_create'),
	path('balance/increase/', balance_increase, name='balance_increase'),
	path('payments/process/', payment_process, name='payment_process'),
	path('payments/done/', payment_done, name='payment_done'),
	path('payments/canceled/', payment_canceled, name='payment_canceled'),
]
