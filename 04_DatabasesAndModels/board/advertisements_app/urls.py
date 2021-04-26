from django.urls import path
from . import views

urlpatterns = [
#path('',views.advertisement_detail, name='advertisement_detail'),
path('advertisements',views.AdvertisementListView.as_view(), 
	name='advertisement_list'),
path('advertisements/<int:pk>',views.AdvertisementDetailView.as_view(), 
	name='advertisement-detail'),
]
