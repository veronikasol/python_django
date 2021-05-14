from django.contrib import admin
from advertisements_app.models import Advertisement, AdvertisementTopic, AdvertisementAuthor

# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
	search_fields = ['description']

@admin.register(AdvertisementTopic)
class AdvertisementTopicAdmin(admin.ModelAdmin):
	pass


@admin.register(AdvertisementAuthor)
class AdvertisementAuthorAdmin(admin.ModelAdmin):
	list_filter = ['name']
