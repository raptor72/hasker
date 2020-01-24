from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='questions_list_url'), 
    path('tags/', tags_list, name='tags_list_url'),
    path('create/', QuestionCreate.as_view(), name='question_create_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('<str:slug>/', QuestionDetail.as_view(), name='question_detail_url'),
]

