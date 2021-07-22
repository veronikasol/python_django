from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_year(value):
	now = datetime.datetime.now().year
	if value < 0 or value > now:
		raise ValidationError(_('%(value)s is not a valid year'),params={'value': value},)

# Create your models here.
class Author(models.Model):
	
	name = models.CharField(max_length=100, verbose_name=_('name'))
	surname = models.CharField(max_length=100, verbose_name=_('surname'))
	year_of_birth = models.PositiveSmallIntegerField(validators=[validate_year], verbose_name=_('date of birth'))

	class Meta:
		ordering = ('surname',)
		verbose_name = _('author')
		verbose_name_plural = _('authors')
	
	def __str__(self):
		return f'{self.name} {self.surname}'



class Book(models.Model):
	
	name = models.CharField(max_length=100, verbose_name=_('book name'))
	isbn = models.CharField(max_length=100, verbose_name=_('ISBN'))
	year_of_publish = models.PositiveSmallIntegerField(validators=[validate_year], verbose_name=_('date of publication'))
	num_of_pages = models.IntegerField(verbose_name=_('number of pages'))
	author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE, verbose_name=_('author'))

	class Meta:
		ordering = ('name',)
		verbose_name = _('book')
		verbose_name_plural = _('books')
	
	def __str__(self):
		return f'{self.name} ({self.author.name} {self.author.surname})'