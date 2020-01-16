from django.shortcuts import render
from .models import Question, Tag

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'hasker/index.html', context={'questions': questions})

def question_detail(request, slug):
    question = Question.objects.get(slug__iexact=slug)
    return render(request, 'hasker/question_detail.html', context={'question': question})

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'hasker/tags_list.html', context={'tags': tags})

def tag_detail(request, slug):
    tag = Tag.objects.get(slug__iexact=slug)
    return render(request, 'hasker/tag_detail.html', context={'tag': tag})

