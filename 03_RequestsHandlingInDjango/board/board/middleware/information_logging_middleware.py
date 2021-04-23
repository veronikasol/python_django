from django.core.exceptions import PermissionDenied
import datetime
import os

class InformationLoggingMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		# файл для логирования в новой директории log с именем log_file.txt: 
		log_dir = os.path.join(os.getcwd(),'log')
		if not os.path.exists(log_dir):
			os.makedirs(log_dir)
		self.log_file = os.path.join(log_dir,'log_file.txt')

	def __call__(self, request):
		
		# ip ресурса с которого запрос идет
		ip = request.META.get('REMOTE_ADDR')
		# время запроса
		log_time = datetime.datetime.now()
		#запрашиваемый URL
		#log_path = request.path
		log_path = request.build_absolute_uri()
		# метод
		log_meth = request.method
		with open(self.log_file, 'a') as logfile:
			logfile.write('date: {}.{}.{}  time: {}:{} url: {} method: {} ip: {}\n'.format(
				log_time.day, log_time.month, log_time.year, log_time.hour, log_time.minute,
				log_path, log_meth, ip))

		response = self.get_response(request)

		return response
