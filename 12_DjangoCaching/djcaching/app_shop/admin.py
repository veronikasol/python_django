from django.contrib import admin
from .models import Category, Product, OrderItem, Offer, Promo, UserAccount

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'available']
	list_editable = ['price', 'available']

@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['user', 'product', 'quantity', 'price']
	list_editable = ['product', 'quantity', 'price']

@admin.register(Offer)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(Promo)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(UserAccount)
class ProductAdmin(admin.ModelAdmin):
	pass