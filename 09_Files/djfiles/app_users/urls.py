from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, profile_edit_view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register', register_view, name='register'),
    path('<int:user_id>', profile_view, name='user_profile'),
    path('edit/<int:user_id>', profile_edit_view, name='profile_edit'),
]