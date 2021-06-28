from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
	last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
	city = forms.CharField(max_length=30, required=False, help_text='Город')
	date_of_birth = forms.DateField(required=False, widget=forms.DateInput, help_text='Дата рождения')
	photo = forms.ImageField(required=False)
	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
	last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')

	class Meta:
		model = Profile
		fields = ['city', 'date_of_birth']