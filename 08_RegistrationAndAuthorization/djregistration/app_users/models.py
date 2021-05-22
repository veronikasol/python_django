from django.db import models
from django.contrib.auth.models import User
from app_news.models import News

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	phone = models.CharField(max_length=12, default=None, null=True, verbose_name='Телефон')
	city = models.CharField(max_length=30, default=None, null=True, verbose_name='Город')
	is_verified = models.BooleanField(default=False, verbose_name='Верифицирован?')
	news = models.ForeignKey(News, default=None, null=True,
		on_delete=models.CASCADE, related_name='profile', verbose_name='новость')

	def __str__(self):
		return f'{self.user.username}: {self.user.first_name} {self.user.last_name} ({self.city})'

	class Meta:
		db_table = 'Profile'