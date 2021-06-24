from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_view, name='posts'),
    path('<int:post_id>', views.post_detail, name='post_detail'),
    path('posts/', views.PostCreateView.as_view(), name='post_form'),
    path('upload_posts', views.upload_posts_view, name='upload_posts'),
]
