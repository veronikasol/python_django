from django.shortcuts import render
from django.http import HttpResponse
import random

course_list = ['Data Scientist', 'Python-разработчик', 'Веб-разработчик', 'Тестировщик', 'Java-разработчик']
course_links = ['https://skillbox.ru/course/profession-data-scientist/',
'https://skillbox.ru/course/profession-python/', 
'https://skillbox.ru/course/profession-webdev/', 
'https://skillbox.ru/course/profession-test/', 
'https://skillbox.ru/course/profession-java/']
course_img_list = ['https://248006.selcdn.ru/LandGen/phone_a2badcf0d1b0145d295d504b2438e437ed0b1323.png', 
'https://248006.selcdn.ru/LandGen/phone_4589beaf332198133164e04e0fb855c2c1368858.png', 
'https://248006.selcdn.ru/LandGen/phone_1483b955a743f9098806cbe6c6d78d306a210b65.png', 
'https://248006.selcdn.ru/LandGen/phone_0b95c9f42ca3ec65c771ec857e7f8193459ca51d.png', 
'https://248006.selcdn.ru/LandGen/phone_477ae814606ca5e5256c683921f40d2d7f29bad4.png']

def advertisement_list(request, *args, **kwargs):
	return render(request,'advertisements/advertisement_list.html', 
		{'courses':course_list})

def advertisement_detail(request,  c_id, **kwargs):
	return render(request,'advertisements/advertisement.html',
		{'course': course_list[c_id-1], 
		'course_link':course_links[c_id-1],
		'course_img':course_img_list[c_id-1],
		'course_price':1000 * random.randint(1,10)})


""" как получить список курсов и все аттрибуты для них с сайта  skillbox:

from selenium import webdriver
browser = webdriver.Firefox()
browser.get('https://skillbox.ru/code/')
course_list_obj = browser.find_elements_by_class_name('card__title')
course_list = []
course_link = []
for c in course_list_obj:
	course_list.append(c.text)
	course_link.append(c.get_attribute('href'))

import requests
import bs4
res = requests.get('https://skillbox.ru/code/')
no_s = bs4.BeautifulSoup(res.text)
pictures = no_s.select('.card__pic')
img_list = [p.get('src') for p in pictures]

"""