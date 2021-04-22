from django.urls import path
from . import views

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('contacts', views.contacts, name='contacts'),
    path('about', views.about, name='about'),
    path('categories', views.categories, name='categories'),
    path('regions/', views.Regions.as_view()),
]
