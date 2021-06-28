from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('register', views.register_view, name='register'),
	path('<int:user_id>', views.profile_view, name='user_profile'),
    path('edit/<int:user_id>', views.profile_edit_view, name='profile_edit'),
]