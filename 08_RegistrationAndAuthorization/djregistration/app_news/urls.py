from django.urls import path
from . import views
from app_news.views import AnotherLoginView, AnotherLogoutView
from app_news.views import NewsCreateView, NewsUpdateView, NewsDeleteView

urlpatterns = [
path('', views.news_list, name='news'),
path('year/<int:year>/', views.news_list, name='news_list_by_date'),
path('tag/<slug:tag_slug>/', views.news_list, name='news_list_by_tag'),
path('<int:news_id>', views.news_detail, name='news_detail'),
path('news/', NewsCreateView.as_view(), name='news_form'),
path('<pk>/edit', NewsUpdateView.as_view(), name='edit_news_form'),
path('<pk>/delete', NewsDeleteView.as_view(), name='delete_news_form'),
path('login', AnotherLoginView.as_view(), name='login'),
path('logout', AnotherLogoutView.as_view(), name='logout'),
]