from django.urls import path
from .views import *

urlpatterns = [
    path('', question_list, name='question_list_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('<str:slug>/', question_detail, name='question_detail_url'),
    path('tag/<str:slug>/', tag_detail, name='tag_detail_url'),

]

