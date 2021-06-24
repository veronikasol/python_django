
from django.db import models

from django.contrib.auth.models import User

class File(models.Model):
	file = models.FileField(blank=True, upload_to='files/', verbose_name='Файлы')
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey('Post', default=None, null=True,
		on_delete=models.CASCADE, related_name='files', verbose_name='публикация')

	def __str__(self):
		return f'{self.file}'


class Post(models.Model):
	title = models.CharField(max_length=1000, verbose_name='Заголовок')
	content = models.TextField(verbose_name='Текст публикации')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
	modified_at = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
	user = models.ForeignKey(User, default=None, null=True,
		on_delete=models.CASCADE, related_name='post')

	def __str__(self):
		return f'{self.title} от {self.created_at.date()} ({self.user.username})'

	class Meta:
		db_table = 'Post'
		ordering = ['-created_at',]