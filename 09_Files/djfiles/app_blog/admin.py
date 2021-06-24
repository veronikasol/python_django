from django.contrib import admin
from .models import Post, File


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title',]


@admin.register(File)
class PostAdmin(admin.ModelAdmin):
	pass