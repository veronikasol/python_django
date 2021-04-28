from django import forms
from news_app.models import News, Comment


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['username', 'content']


class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = '__all__'
