from django.shortcuts import render
import random
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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


class AdvertisementListView(ListView):
	model = Advertisement
	template_name = 'advertisement_list.html'
	context_object_name = 'advertisement_list'
	queryset = Advertisement.objects.all()[:5]


class AdvertisementDetailView(DetailView):
	model = Advertisement