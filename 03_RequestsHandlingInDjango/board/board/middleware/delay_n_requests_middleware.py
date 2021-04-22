from django.core.exceptions import PermissionDenied
import time

class DelayNRequestsMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response
		self.num_of_calls = 1
		self.n = 10

	def __call__(self, request):
		
		if self.num_of_calls % self.n == 0:
			time.sleep(5)
		self.num_of_calls += 1

		response = self.get_response(request)

		return response
