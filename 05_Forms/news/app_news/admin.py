from django.contrib import admin
from app_news.models import News, Comment

class CommentInline(admin.TabularInline):
	model = Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	search_fields = ['content']
	inlines = [
	CommentInline,
	]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_filter = ['username']
	
