from django.core.exceptions import PermissionDenied
import time

class MorethanKRequestsMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		self.ip_list = {}
		self.denied_ips =[]

	def __call__(self, request):
		
		# ip ресурса с которого запрос идет
		ip = request.META.get('REMOTE_ADDR')

		if ip in self.denied_ips:
			raise PermissionDenied

		# словарь в котором ip - ключ [стартовое время, количество запросов] - список значений
		self.ip_list.setdefault(ip,[0,0])
		# если это первый запрос - засекаем время
		if self.ip_list[ip][1] == 0:
			self.ip_list[ip][0] = time.time()
			self.ip_list[ip][1] += 1
		else:
			self.ip_list[ip][1] += 1
			t = time.time()
			# если количество запросов больше 5 за 5 секунд
			if self.ip_list[ip][1] >= 10 and t-self.ip_list[ip][0] <= 5:
				self.denied_ips.append(ip)
				raise PermissionDenied

		response = self.get_response(request)

		return response
