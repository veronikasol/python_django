from django.urls import path
from . import views
from news_app.views import NewsFormView

urlpatterns = [
path('', views.NewsListView.as_view(), name='news'),
path('<int:news_id>', views.news_detail, name='news_detail'),
path('news', NewsFormView.as_view(), name='news_form')
]