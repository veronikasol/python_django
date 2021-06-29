from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, MultiFileForm



# Create your views here.
def posts_view(request):
	
	return render(request,'app_blog/posts.html')


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