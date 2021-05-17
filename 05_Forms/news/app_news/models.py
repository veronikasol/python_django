from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
	title = models.CharField(max_length=1000, verbose_name='Заголовок новости')
	content = models.TextField(verbose_name='Тескт новости')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
	modified_at = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
	is_active = models.BooleanField(verbose_name='Активна?')

	def __str__(self):
		return f'{self.title}, от: {self.created_at.date()} ({"активна" if self.is_active else "неактивна"})'


	class Meta:
		db_table = 'News'
		ordering = ['created_at',]


class Comment(models.Model):
	username = models.CharField(max_length=20, verbose_name='имя пользователя')
	#Измените таблицу “Комментарий” - добавьте поле user c FK связью с таблицей User
	user = models.ForeignKey(User, default=None, null=True,
		on_delete=models.CASCADE, related_name='comments', verbose_name='пользователь')
	content = models.TextField(verbose_name='текст комментария')
	news = models.ForeignKey('News', default=None, null=True,
		on_delete=models.CASCADE, related_name='comments', verbose_name='новость')

	def __str__(self):
		return f'От {self.username}: {self.content[:15]}...'

	class Meta:
		db_table = 'Comment'