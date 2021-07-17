from django.conf.urls import url
from api import views

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Hasker API')


urlpatterns = [
    url('get_schema/', schema_view),
    url('get_users/', views.get_users),
    url('get_index/', views.get_index),
]