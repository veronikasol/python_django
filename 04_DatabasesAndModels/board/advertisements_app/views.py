from django.shortcuts import render
import random
from advertisements_app.models import Advertisement

def advertisement_detail(request, *args, **kwargs):
	choise = random.randint(1,Advertisement.objects.count())
	while not Advertisement.objects.filter(pk=choise).exists():
		choise = random.randint(1,Advertisement.objects.count())
	chosen = Advertisement.objects.get(pk=choise)
	chosen.views_count += 1
	chosen.save()
	return render(request,'advertisements_app/advertisement_detail.html',
		{'ad':chosen})