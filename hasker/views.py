from django.shortcuts import render


def question_list(request):
    n = ['A', 'B', 'C', 'D']
    return render(request, 'hasker/index.html', context={'names': n})
