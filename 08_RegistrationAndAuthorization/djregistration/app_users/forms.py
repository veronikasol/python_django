from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
	
	first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
	last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
	phone = forms.CharField(max_length=12, required=False, help_text='Телефон')
	city = forms.CharField(max_length=30, required=False, help_text='Город')
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields =  UserCreationForm.Meta.fields + ('first_name', 'last_name')

class ProfileEditForm(forms.ModelForm):

	first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
	last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
	class Meta:
		model = Profile
		fields = ['phone', 'city']