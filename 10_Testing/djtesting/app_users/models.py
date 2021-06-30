from django.db import models
from django.contrib.auth.models import User
from app_blog.models import Post

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
	city = models.CharField(max_length=30, default=None, null=True, verbose_name='Город')
	photo = models.ImageField(blank=True, verbose_name='Аватар')
	post = models.ForeignKey(Post, default=None, null=True,
		on_delete=models.CASCADE, related_name='profile', verbose_name='публикация')

	def __str__(self):
		return f'{self.user.username}: {self.user.get_full_name()} ({self.city})'

	class Meta:
		db_table = 'Profile'