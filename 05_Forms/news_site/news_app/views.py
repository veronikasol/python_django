from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views import View
from news_app.models import News, Comment
from news_app.forms import CommentForm, NewsForm

class NewsListView(ListView):
	model = News
	template_name = 'news_list.html'
	context_object_name = 'news_list'


def news_detail(request, news_id):
	news = News.objects.get(pk=news_id) # метод get y News
	comments = news.comments.all()
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.news = news
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request,'news_app/news_detail.html', {'news':news, 'comments':comments,
		'new_comment':new_comment,'comment_form':comment_form})


class NewsFormView(View):
	
	def get(self,request):
		news_form = NewsForm()
		return render(request,'news_app/news_form.html', context={'news_form':news_form})

	def post(self, request):
		news_form = NewsForm(request.POST)
		if news_form.is_valid():
			News.objects.create(**news_form.cleaned_data)
			return HttpResponseRedirect('/')
		return render(request, 'news_app/news_form.html', context={'news_form':news_form})