from django.db import models

class Advertisement(models.Model):
	title = models.CharField(max_length=1500)
	description = models.TextField()