from django.urls import path
from .views import product_list, product_detail, user_account

urlpatterns = [
	path('', product_list, name='product_list'),
	path('<int:pk>/', product_detail, name='product_detail'),
	path('<slug:category_slug>/', product_list, name='product_list_by_category'),
	path('account/<int:user_id>', user_account, name='user_account'),
]