from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.views.generic import View
from .utils import *
from django.views import generic
from .forms import TagForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(generic.ListView):
    template_name='hasker/index.html'
    context_object_name='questions'

    def get_queryset(self):
        return Question.objects.all()


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'hasker/tags_list.html', context={'tags': tags})


class QuestionDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Question
    redirect_url = 'accounts:login'
    template = 'hasker/question_detail.html'


class TagDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Tag
    redirect_url = 'accounts:login'
    template = 'hasker/tag_detail.html'


#class TagCreate(View):
#    def get(self, request):
#        form = TagForm()
#        return render(request, 'hasker/tag_create.html', context={'form': form})
#
#    def post(self, request):
#        bound_form = TagForm(request.POST)
#        if bound_form.is_valid():
#            new_tag = bound_form.save()
#            return redirect(new_tag)
#        return render(request, 'hasker/tag_create.html', context={'form': bound_form})


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model  = TagForm
    template = 'hasker/tag_create.html'

class QuestionCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model  = QuestionForm
    template = 'hasker/question_create.html'


#class QuestionCreate(View):
#    def get(self, request):
#        form = QuestionForm
#        return render(request, 'hasker/question_create.html', context={'form': form})
#
#    def post(self, request):
#        bound_form = QuestionForm(request.POST)
#        if bound_form.is_valid():
#            new_question = bound_form.save()
#            return redirect(new_question)
#        return render(request, 'hasker/question_create.html', context={'form': bound_form})






