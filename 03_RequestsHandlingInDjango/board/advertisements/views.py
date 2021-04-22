from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def advertisement_list(request, *args, **kwargs):
    advertisements = [
        'Мастер на час',
        'Выведение из запоя',
        'Услуги экскаватора-погрузчика, гидромолота, ямобура'
    ]
    advertisements_1 = [
        'Стяжка',
        'Малярка',
        'Штукатурка'
    ]
    advertisements_2 = [
        'Снятие порчи',
        'Гадание по руке',
        'Любой заговор и снятие заговора',
        'Любой приворот и снятие приворота'
    ]
    return render(request, 'advertisements/advertisement_list.html',
        {'advertisements': advertisements,
        'advertisements_1': advertisements_1, 
        'advertisements_2': advertisements_2})

def contacts(request, *args, **kwargs):
    contact_list = [['sales@company.com','+88007081945'],]
    
    return render(request, 'advertisements/contacts.html', 
        {'email':contact_list[0][0], 'tel':contact_list[0][1]})

def about(request, *args, **kwargs):
    company_list = [['Бесплатные объявления', 'Бесплатные объявления в вашем городе!']]
    
    return render(request, 'advertisements/about.html', {'name': company_list[0][0],
        'description':company_list[0][1]})

def categories(request, *args, **kwargs):
    category_list = ['автомобиль', 'ремонт', 'магия']
    return render(request, 'advertisements/categories.html', {'category_list': category_list})

#@method_decorator(csrf_exempt,name='dispatch')
class Regions(View):

    def get(self,request):
        region_list = ['Москва', 'Московская область', 'республика Алтай', 'Вологодская область']
        return render(request, 'advertisements/regions.html', {'region_list': region_list})
    @csrf_exempt
    def post(self,request):
        return HttpResponse(content='регион успешно создан', content_type=None, status=200)