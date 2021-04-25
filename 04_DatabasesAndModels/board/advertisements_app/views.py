from django.shortcuts import render
import random
from advertisements_app.models import Advertisement

def advertisement_detail(request, *args, **kwargs):
	ads = Advertisement.objects.all()
	choise = random.randint(1,5)
	chosen = Advertisement.objects.get(pk=choise)
	chosen.views_count += 1
	chosen.save()
	return render(request,'advertisements_app/advertisement_detail.html',
		{'ad':ads[choise]})