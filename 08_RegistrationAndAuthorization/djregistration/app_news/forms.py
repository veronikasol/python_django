from django import forms
from app_news.models import News, Comment


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']


class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = '__all__'
