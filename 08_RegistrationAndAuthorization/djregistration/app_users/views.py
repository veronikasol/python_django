from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app_users.forms import RegisterForm, ProfileEditForm
from app_users.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView



def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			phone = form.cleaned_data.get('phone')
			city = form.cleaned_data.get('city')
			Profile.objects.create(
				user=user,
				phone=phone,
				city=city)
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = RegisterForm()
	return render(request,'app_users/register.html', {'form':form})

def user_profile_view(request, user_id):
	user = User.objects.get(pk=user_id)
	if Profile.objects.filter(user=user).exists():
		profile = Profile.objects.get(user=user)
	else:
		profile = {}
	news = user.news.filter(is_active=True).count()
	return render(request,'app_users/user_profile.html', 
		{'news':news, 'user_id':user_id, 'user': user, 'profile':profile})


def edit_profile_view(request, user_id):
	user = User.objects.get(pk=user_id)
	# если у пользователя был профиль - отображаем его:
	if Profile.objects.filter(user=user).exists():
		user_profile = Profile.objects.get(user=user)
	# если профиля не было - создаем
	else:
		user_profile = Profile.objects.create(user=user)
	if request.method == 'POST':
		form = ProfileEditForm(request.POST, instance=user_profile)
		if form.is_valid():
			form.save()
			phone = form.cleaned_data.get('phone')
			city = form.cleaned_data.get('city')
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.save()
			Profile.objects.filter(user_id=user_id).update(phone=phone,city=city)
			return HttpResponseRedirect('../'+str(user_id))
	else:
		form = ProfileEditForm({
			'first_name': user.first_name, 
			'last_name': user.last_name,
			'phone': user_profile.phone,
			'city': user_profile.city})
	return render(request,'app_users/edit_user_profile.html',
		{'user_id':user_id, 'user': user, 'form': form})

class ApproveProfileListView(PermissionRequiredMixin, ListView):
	# Только у модераторов есть разрешение на просмотр флага верификации всех пользователей
	model = Profile
	template_name = 'app_users/approve_profile_list.html'
	context_object_name = 'profile_list'
	permission_required = 'auth.change_group'


class ApproveProfileUpdateView(PermissionRequiredMixin, UpdateView):
	# Только у модераторов есть разрешение на изменение флага верификации,
	# они могут переводить пользователей в группу верифицированных
	model = Profile
	fields = ['is_verified']
	template_name = 'app_users/approve_profile.html'
	success_url = reverse_lazy('approve_profile_list')
	permission_required = 'auth.change_group'

	def post(self, request, **kwargs):
		"""
		Переопределяет поведение post, чтобы добавить пользователя,
		для которого происходит верификации, в группу верифицированных
		"""
		self.object = self.get_object()
		user = User.objects.get(pk=self.object.user_id)
		verified_user = Group.objects.get(name='verified_user')
		if self.object.is_verified:
			user.groups.add(verified_user)
		else:
			user.groups.remove(verified_user)
		user.save()
		return super().post(request, **kwargs)