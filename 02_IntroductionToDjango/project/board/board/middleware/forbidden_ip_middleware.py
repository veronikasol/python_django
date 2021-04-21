from django.core.exceptions import PermissionDenied

class ForbiddenIPMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		
		#allowed_ips = ['127.0.0.1']
		forbidden_ips = ['127.0.0.2']
		ip = request.META.get('REMOTE_ADDR')
		if ip in forbidden_ips:
			raise PermissionDenied

		response = self.get_response(request)

		return response
