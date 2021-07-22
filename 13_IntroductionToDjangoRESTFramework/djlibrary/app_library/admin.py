from django.contrib import admin
from .models import Author, Book

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ['name', 'surname', 'year_of_birth']

@admin.register(Book)
class AuthorAdmin(admin.ModelAdmin):
	pass