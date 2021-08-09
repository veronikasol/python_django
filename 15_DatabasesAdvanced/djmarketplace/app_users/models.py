from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Date of birth'))
	city = models.CharField(max_length=30, default=None, null=True, verbose_name=_('City'))
	photo = models.ImageField(blank=True, verbose_name=_('Avatar'))
	
	def __str__(self):
		return f'{self.user.username}: {self.user.get_full_name()} ({self.city})'

	class Meta:
		db_table = 'Profile'
		verbose_name_plural = _('profiles')
		verbose_name = _('profile')