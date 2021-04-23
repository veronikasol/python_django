from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView

class Index(TemplateView):
    template_name = 'advertisements/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ['автомобиль', 'ремонт', 'магия']
        context['regions'] = ['Москва', 'Московская область', 'республика Алтай', 'Вологодская область']
        return context

    def post(self,request):
        return HttpResponse('OK')


class AdvertisementList(View):

    def __init__(self):
        self.count = 0
    
    def get(self,request):
        advertisements = ['Мастер на час','Выведение из запоя',
        'Услуги экскаватора-погрузчика, гидромолота, ямобура']
        advertisements_1 = ['Стяжка','Малярка','Штукатурка']
        advertisements_2 = ['Снятие порчи','Гадание по руке',
        'Любой заговор и снятие заговора','Любой приворот и снятие приворота']
        
        return render(request, 'advertisements/advertisement_list.html',
            {'advertisements': advertisements,
            'advertisements_1': advertisements_1, 
            'advertisements_2': advertisements_2, 'count':self.count})
   
    def post(self,request):
        self.count += 1
        return HttpResponse('Запрос на создание новой записи успешно выполнен\n')


class Contacts(TemplateView):

    template_name = 'advertisements/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = 'sales@company.com'
        context['tel'] = '+88007081945'
        return context

class About(TemplateView):

    template_name = 'advertisements/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Бесплатные объявления'
        context['description'] = 'Бесплатные объявления в вашем городе!'
        return context

def categories(request, *args, **kwargs):
    category_list = ['автомобиль', 'ремонт', 'магия']
    return render(request, 'advertisements/categories.html', {'category_list': category_list})

class Regions(View):

    def get(self,request):
        region_list = ['Москва', 'Московская область', 'республика Алтай', 'Вологодская область']
        return render(request, 'advertisements/regions.html', {'region_list': region_list})
  
    def post(self,request):
        return HttpResponse('регион успешно создан\n')