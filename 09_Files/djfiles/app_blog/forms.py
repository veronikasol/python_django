from django import forms
from .models import Post, File

class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ['title','content',]

class MultiFileForm(forms.Form):
	file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}), 
		required=False, help_text='Загрузите файлы')
