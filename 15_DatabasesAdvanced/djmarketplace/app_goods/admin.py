from django.contrib import admin
from .models import Category, Product, OrderItem, Offer, Promo, UserAccount
from .models import Shop, Content, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(Offer)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(Promo)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(UserAccount)
class ProductAdmin(admin.ModelAdmin):
	pass

@admin.register(Shop)
class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}


@admin.register(Content)
class ProductAdmin(admin.ModelAdmin):
	pass


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
	pass