from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('advertisement', views.AdvertisementList.as_view(), name='advertisement_list'),
    path('contacts', views.Contacts.as_view(), name='contacts'),
    path('about', views.About.as_view(), name='about'),
    path('categories', views.categories, name='categories'),
    path('regions', views.Regions.as_view(), name='regions'),
]
