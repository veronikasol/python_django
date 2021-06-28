from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts_view, name='posts'),
    ]