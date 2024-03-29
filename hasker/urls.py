from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='questions_list_url'), 
    # path('tags/', tags_list, name='tags_list_url'),
    path('tags/', TagsListView.as_view(), name='tags_list_url'),
    path('create/', QuestionCreate.as_view(), name='question_create_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    # path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/', tag_detail, name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('<str:slug>/', question_detail, name='question_detail_url'),
    path('<str:slug>/update/', QuestionUpdate.as_view(), name='question_update_url'),
    path('<str:slug>/delete/', QuestionDelete.as_view(), name='question_delete_url'),
    path('vote/<str:answer_id>/', vote_answer, name='vote_answer_url'),
    path('correct/<str:answer_id>/', mark_as_correct, name='mark_as_correct_url'),
]

