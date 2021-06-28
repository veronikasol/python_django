from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, ProfileEditForm
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def register_view(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST,request.FILES)
		if form.is_valid():
			user = form.save(commit=False)
			date_of_birth = form.cleaned_data.get('date_of_birth')
			city = form.cleaned_data.get('city')
			photo = form.cleaned_data.get('photo')
			user.set_password(form.cleaned_data['password1'])
			user.save()
			Profile.objects.create(
				user=user,
				date_of_birth=date_of_birth,
				city=city, photo=photo)
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = RegisterForm()
	return render(request,'app_users/register.html', {'form':form})

def profile_view(request, user_id):
	user = User.objects.get(pk=user_id)
	if Profile.objects.filter(user=user).exists():
			profile = Profile.objects.get(user=user)
	else:
		profile = {}
	return render(request, 'app_users/profile.html', {'profile':profile})


def profile_edit_view(request, user_id):
	user = User.objects.get(pk=user_id)
	if Profile.objects.filter(user=user).exists():
		user_profile = Profile.objects.get(user=user)
	else:
		user_profile = Profile.objects.create(user=user)
	if request.method == 'POST':
		form = ProfileEditForm(request.POST, instance=user_profile)
		if form.is_valid():
			form.save()
			city = form.cleaned_data.get('city')
			date_of_birth = form.cleaned_data.get('date_of_birth')
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.save()
			Profile.objects.filter(user_id=user_id).update(
				city=city, date_of_birth=date_of_birth)
			return HttpResponseRedirect('../'+str(user_id))
	else:
		form = ProfileEditForm({
			'first_name': user.first_name, 
			'last_name': user.last_name,
			'date_of_birth': user_profile.date_of_birth,
			'city': user_profile.city})
	return render(request,'app_users/profile_edit.html',
		{'user_id':user_id, 'user': user, 'form': form})