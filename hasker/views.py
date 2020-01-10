from django.shortcuts import render
from .models import Question

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'hasker/index.html', context={'questions': questions})


def question_detail(request, slug):
    question = Question.objects.get(slug__iexact=slug)
    return render(request, 'hasker/question_detail.html', context={'question': question})

