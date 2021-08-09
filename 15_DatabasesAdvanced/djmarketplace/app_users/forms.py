from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text=_('Name'))
	last_name = forms.CharField(max_length=30, required=False, help_text=_('Surname'))
	city = forms.CharField(max_length=30, required=False, help_text=_('City'))
	date_of_birth = forms.DateField(required=False, widget=forms.DateInput, 
		help_text=_('Date of birth'))
	photo = forms.ImageField(required=False)
	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')


class ProfileEditForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=False, help_text=_('Name'))
	last_name = forms.CharField(max_length=30, required=False, help_text=_('Surname'))

	class Meta:
		model = Profile
		fields = ['city', 'date_of_birth', 'photo']