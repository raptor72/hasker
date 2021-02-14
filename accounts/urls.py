from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name = "accounts"
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view()),
    path('register/', user_registration, name='register'),
    path('settings/', user_settings, name='user_settings_url'),
]


