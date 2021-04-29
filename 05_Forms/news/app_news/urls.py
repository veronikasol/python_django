from django.urls import path
from . import views
from app_news.views import NewsFormView, EditNewsFormView

urlpatterns = [
path('', views.NewsListView.as_view(), name='news'),
path('<int:news_id>', views.news_detail, name='news_detail'),
path('news', NewsFormView.as_view(), name='news_form'),
path('news/<int:news_id>', EditNewsFormView.as_view(), name='edit_news_form'),
]