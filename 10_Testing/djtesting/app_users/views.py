from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm

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
			#return redirect('/')
			return HttpResponse('OK')
	else:
		form = RegisterForm()
	return render(request,'app_users/register.html', {'form':form})