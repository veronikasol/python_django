from django.urls import path

from app_users.views import restore_password, AnotherLoginView


urlpatterns = [
    path('restore_password/', restore_password, name='restore_password'),
    path('login/', AnotherLoginView.as_view(), name='login'),
]
