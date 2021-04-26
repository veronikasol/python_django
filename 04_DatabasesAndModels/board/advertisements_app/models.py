from django.db import models


class Advertisement(models.Model):
	title = models.CharField(max_length=1500, db_index=True, verbose_name='заголовок')
	description = models.TextField(verbose_name='описание')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
	price = models.IntegerField(default=0, verbose_name='цена')
	views_count = models.IntegerField(default=0,verbose_name='количество просмотров')
	status = models.ForeignKey('AdvertisementStatus', default=None, null=True,
		on_delete=models.CASCADE, related_name='ads', verbose_name='статус')
	ad_type = models.ForeignKey('AdvertisementType', default=None, null=True,
		on_delete=models.CASCADE, related_name='ads', verbose_name='тип')
	ad_topic = models.ForeignKey('AdvertisementTopic', default=None, null=True,
		on_delete=models.CASCADE, related_name='ads', verbose_name='рубрика')
	ad_author = models.ForeignKey('AdvertisementAuthor', default=None, null=True,
		on_delete=models.CASCADE, related_name='ads', verbose_name='автор')

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'Advertisements'
		ordering = ['title']


class AdvertisementStatus(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class AdvertisementType(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class AdvertisementTopic(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class AdvertisementAuthor(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	telephone = models.CharField(max_length=12)

	def __str__(self):
		return self.name
