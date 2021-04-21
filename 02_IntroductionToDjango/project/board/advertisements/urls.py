from django.urls import path
from . import views


urlpatterns = [
    path("", views.advertisement_list, name='advertisement_list'),
    path("advertisement/<int:c_id>", views.advertisement_detail, name='advertisement_detail'),
]