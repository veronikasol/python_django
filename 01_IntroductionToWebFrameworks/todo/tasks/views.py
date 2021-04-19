from django.http import HttpResponse

from django.views import View
import random


class ToDoView(View):

    def get(self, request, *args, **kwargs):
    	elements = ['Помыть посуду',' Убрать со стола', 'Покормить кота',
    	'Погулять', 'Поработать', 'Послушать подкаст', 'Почитать газету', 
    	'Установить python', 'Установить django', 'Запустить сервер', 
    	'Порадоваться результату', 'Порадоваться новому дню']
    	already_in = []
    	to_do_list = '<ul>'
    	for i in range(5):
    		choice = random.randint(0,len(elements)-1)
    		while choice in already_in:
    			choice = random.randint(0,len(elements)-1)
    		to_do_list += '<li>' + elements[choice] + '</li>'
    		already_in.append(choice)
    	to_do_list += '</ul>'
    	return HttpResponse(to_do_list)