from django.contrib import admin
from advertisements_app.models import Advertisement

# Register your models here.
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
	pass