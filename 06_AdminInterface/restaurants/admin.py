from django.contrib import admin
from .models import Restaurant, Waiter


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
	fieldsets = (
		('основые сведения', {'fields':('name','description')}),
		('персонал', {'fields':('count_of_employers', 'director', 'chef')}),
		('контакты', {'fields':('phone', 'country', 'city', 'street', 'house')}),
		('меню', {'fields':('serves_hot_dogs', 'serves_pizza', 'serves_sushi', 
			'serves_burgers', 'serves_coffee', 'serves_donats'),
		'description':'наличие блюд'})
		)


@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
	fieldsets = (
		('основые сведения', {'fields':('restaurant','first_name', 'last_name', 'age', 'sex')}),
		('контакты', {'fields':('country', 'city', 'street', 'house', 'apartment')}),
		('квалификация', {'fields':('seniority', 'education', 'cources'),
		'description':'образование и курсы повышения квалификации'})
		)