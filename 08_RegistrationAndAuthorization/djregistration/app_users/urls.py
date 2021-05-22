from django.urls import path
from .views import register_view, user_profile_view
from .views import edit_profile_view
from .views import ApproveProfileListView, ApproveProfileUpdateView


urlpatterns = [
path('register', register_view, name='register'),
path('<int:user_id>', user_profile_view, name='user_profile'),
path('edit/<int:user_id>', edit_profile_view, name='edit_user_profile'),
path('approve', ApproveProfileListView.as_view(), name='approve_profile_list'),
path('approve/<pk>', ApproveProfileUpdateView.as_view(), name='approve_profile'),
]