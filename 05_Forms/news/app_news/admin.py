from django.contrib import admin
from app_news.models import News, Comment


class CommentInline(admin.TabularInline):
	model = Comment

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	#в списке новостей выведите все ее поля, кроме текста новости
	readonly_fields = ('created_at','modified_at')
	exclude = ['content']
	#реализуйте возможность фильтрации новостей по флагу активности
	list_filter = ['is_active']
	# добавьте 2 действия для массового перевода новостей: в статус “активно” и статус “неактивно”
	actions = ['mark_as_active', 'mark_as_inactive']
	#добавьте возможность просматривать и редактировать комментарии к новости с помощью TabularInline
	inlines = [CommentInline,]
	
	def mark_as_active(self,request,queryset):
		queryset.update(is_active=True)

	def mark_as_inactive(self,request,queryset):
		queryset.update(is_active=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_filter = ['username']
	# добавьте действие для комментариев, 
	# которое будет проставлять текст выбранным комментариям “Удалено администратором”.
	actions = ['deleted_by_admin',]

	def deleted_by_admin(self,request,queryset):
		queryset.update(content='Удалено администратором')

	
