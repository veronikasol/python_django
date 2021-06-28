from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def posts_view(request):
	
	return render(request,'app_blog/posts.html')