from django import template

register = template.Library()

@register.filter(name='convert_to_usd')
def convert(value):
	"""переводит значение цены в рублях в значение в долларах
	с указанием курса ЦБ на текущую дату
	"""
	import bs4
	import requests
	
	url = 'http://www.cbr.ru/scripts/XML_daily.asp'
	result = requests.get(url)
	no_bs = bs4.BeautifulSoup(result.text,'lxml')
	dollar = no_bs.select('#R01235 > value')[0].getText()
	dollar = float(dollar.replace(',','.'))
	return ('{:.2f} USD по курсу 1:{:.2f}'.format(float(value)//dollar, dollar ))