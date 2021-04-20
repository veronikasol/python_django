from django.shortcuts import render
from django.http import HttpResponse

def advertisement_list(requset, *args, **kwargs):
	return HttpResponse('<ul>'
		'<li>Любая работа</li>'
		'<li>Штукатурка</li>'
		'<li>Малярка</li>'
		'<li>Стяжка</li>'
		'</ul>'
		)

def advertisement_detail(requset, *args, **kwargs):
	return HttpResponse(
		'<h3>Более детельное описание объявления</h3>'
		'<p>Мы все сделаем. Выбирайте нас.</p>'
		)

