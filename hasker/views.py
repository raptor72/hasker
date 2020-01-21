from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from django.views.generic import View
from .utils import ObjectDetailMixin
from django.views import generic


class IndexView(generic.ListView):
    template_name='hasker/index.html'
    context_object_name='questions'

    def get_queryset(self):
        return Question.objects.all()


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'hasker/tags_list.html', context={'tags': tags})


class QuestionDetail(ObjectDetailMixin, View):
    model = Question
    template = 'hasker/question_detail.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'hasker/tag_detail.html'
