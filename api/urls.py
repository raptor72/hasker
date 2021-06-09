from django.conf.urls import url
from api import views

urlpatterns = [
    url('get_users/', views.get_users),
]