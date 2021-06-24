from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, File
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import MultiFileForm, PostForm
import csv
from io import StringIO

# Create your views here.

def posts_view(request):
	object_list = Post.objects.all()
	return render(request, 'app_blog/posts.html', {'post_list':object_list})


def post_detail(request,post_id):
	post = Post.objects.get(pk=post_id)
	files = post.files.all()
	return render(request, 'app_blog/post_detail.html', {'post':post, 'files':files})


class PostCreateView(View, LoginRequiredMixin):
	
	def get(self,request):
		post_form = PostForm()
		file_form = MultiFileForm()
		return render(request,'app_blog/post_form.html', context={'post_form':post_form, 'file_form':file_form})

	def post(self, request):
		post_form = PostForm(request.POST)
		file_form = MultiFileForm(request.POST, request.FILES)
		if post_form.is_valid():
			cd = post_form.cleaned_data
			new_post = post_form.save(commit=False)
			new_post.user = request.user
			new_post.save()
			if file_form.is_valid():
				files = request.FILES.getlist('file_field')
				for f in files:
					instance = File(file=f, post=new_post)
					instance.save()
			return HttpResponseRedirect('/')
		return render(request, 'app_blog/post_form.html', context={'post_form':post_form, 'file_form':file_form})

@login_required
def upload_posts_view(request):
	if request.POST and request.FILES:
		csvfile = request.FILES['csv_file']
		file = csvfile.read().decode('utf-8')
		csv_data = csv.reader(StringIO(file), delimiter=',')
		user = request.user
		for row in csv_data:
			Post.objects.create(user=user, content=row[0])
		return HttpResponseRedirect('/')
		#return HttpResponse('OK')
	context = {}
	return render(request, 'app_blog/multiple_post.html', context=context)