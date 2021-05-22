from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views import View
from app_news.models import News, Comment
from app_news.forms import CommentForm, NewsForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from taggit.models import Tag


def news_list(request, tag_slug=None, year=None, month=None, day=None):
	user = request.user
	object_list = News.objects.all()
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])
	if year:
		object_list = object_list.filter(created_at__year=year)
	if not user.has_perm('app_news.change_news'):
		# Обычному пользователю доступны только активные новости
		object_list = object_list.filter(is_active=True)
	# Страница со списком новостей (главная) будет отображаться по-разному
	# для пользователей из разных групп.
	# может добавлять новость и изменять их (группа verified_user и moderator)
	add_perm = user.has_perm('app_news.add_news')
	# может менять флаг верификации для пользователей (группа moderator)
	verify_perm = user.groups.filter(name='moderator').exists()
	return render(request, 'app_news/news_list.html', {
		'news_list':object_list, 'add_perm': add_perm,
		'verify_perm': verify_perm,'tag': tag, 'year': year})


def news_detail(request, news_id):
	news = News.objects.get(pk=news_id)
	# Если у пользователя есть разрешение на редактирование - 
	# ему будет доступно редактирование и удаление новости
	perm = request.user.has_perm('app_news.change_news')
	comments = news.comments.all()
	new_comment = None
	comment_user = request.user
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.news = news
			if comment_user.is_authenticated:
				new_comment.user = comment_user
				new_comment.username = comment_user.username
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request,'app_news/news_detail.html', {'news':news, 'news_id':news_id,
		'comments':comments, 'new_comment':new_comment,'comment_form':comment_form, 'perm':perm})


class AnotherLoginView(LoginView):
	template = 'app_news/login.html'


class AnotherLogoutView(LogoutView):
	next_page = '/'

# Дженерик классы для добавления, редактирования и удаления новостей
# в каждом виде предусматривается, 
# что пользователь обладает разрешениями для выполнения этих действий
class NewsCreateView(PermissionRequiredMixin, CreateView):
	model = News
	fields = ['title','content']
	template_name = 'app_news/news_form.html'
	success_url = reverse_lazy('news')
	permission_required = 'app_news.add_news'

	def form_valid(self, form):
		# Переопределяет поведение, чтобы добавить пользователя, создавшего новость
		form.instance.user = self.request.user
		return super().form_valid(form)

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
	model = News
	fields = ['title', 'content', 'is_active']
	template_name = 'app_news/news_form.html'
	success_url = reverse_lazy('news')
	permission_required = 'app_news.change_news'

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
	model = News
	template_name = 'app_news/news_delete.html'
	success_url = reverse_lazy('news')
	permission_required = 'app_news.delete_news'