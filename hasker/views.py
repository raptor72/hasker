import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.views.generic import View
from .utils import *
from django.urls import reverse
from django.views import generic
from .forms import TagForm, QuestionForm, AnswerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from hasker.utils import fbv_paginator


class IndexView(generic.ListView):
    template_name = 'hasker/index.html'
    context_object_name = 'questions'
    paginate_by = 8

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Question.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        return Question.objects.all()


class TagsListView(generic.ListView):
    model = Tag
    context_object_name = 'tag'
    queryset = Tag.objects.all()
    template_name = 'hasker/tags_list.html'
    paginate_by = 2


def tags_list(request):
    tags = Tag.objects.all()
    context = fbv_paginator(request, tags, 3, 'page')
    return render(request, 'hasker/tags_list.html', context=context)


@login_required
def question_detail(request, slug):
    user = request.user
    question = get_object_or_404(Question, slug=slug)
    if request.method == 'POST' and user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Answer.objects.create(question=question, content=content, user=user)
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        answers = question.answer_set.all()
        has_correct_mark = question.answer_set.filter(is_correct=True).first()
        context = fbv_paginator(request, answers, 8, 'page')
        context.update({'has_correct_mark': has_correct_mark})
        if question.author == user:
            context.update({'question': question,})
            return render(request, 'hasker/question_detail.html', context=context)
        form = AnswerForm()
        user_can_vote = question.user_can_vote(request.user)
        if user_can_vote:
            context.update({'form': form, 'question': question, 'user_can_vote': user_can_vote})
            return render(request, 'hasker/question_detail.html', context=context)
        else:
            choised_answer_id = question.vote_set.filter(user=user).first().answer.id
            context.update({'form': form, 'question': question, 'choised_answer_id': choised_answer_id})
            return render(request, 'hasker/question_detail.html', context=context)


class TagDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Tag
    redirect_url = 'accounts:login'
    template = 'hasker/tag_detail.html'


@login_required
def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    questions = tag.questions.all()
    context = fbv_paginator(request, questions, 5, 'page')
    context.update({'tag': tag})
    return render(request, 'hasker/tag_detail.html', context=context)


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'hasker/tag_create.html'


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'hasker/tag_update_form.html'


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'hasker/tag_delete_form.html'
    redirect_url = 'tags_list_url'


class QuestionCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = QuestionForm
    template = 'hasker/question_create.html'


class QuestionUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Question
    model_form = QuestionForm
    template = 'hasker/question_update_form.html'


class QuestionDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Question
    template = 'hasker/question_delete_form.html'
    redirect_url = 'questions_list_url'


def vote_answer(request, answer_id):
    user = request.user
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question
    user_can_vote = question.user_can_vote(user)
    if request.method == 'GET' and user.is_authenticated:
        if user_can_vote:
            Vote.objects.create(question=question, user=user, answer=answer)
        else:
            vote = Vote.objects.filter(question=question, user=user).first()
            vote.delete()
    return HttpResponseRedirect(question.get_absolute_url())


def mark_as_correct(request, answer_id):
    user = request.user
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question
    has_correct_mark = question.answer_set.filter(is_correct=True).first()

    if request.method == 'GET' and user.is_authenticated:
        if user == question.author and not has_correct_mark:
            logging.warning('Answer can be market as correct')
            answer.is_correct = True
            answer.save()
        if user == question.author and has_correct_mark and answer.is_correct:
            logging.warning('Correct mark can be removed for this answer')
            answer.is_correct = False
            answer.save()
        if user == question.author and has_correct_mark and not answer.is_correct:
            logging.error('Question already have correct mark in another answer')
        else:
            logging.error('Requested user can not marker answer as correct for this question')
        return HttpResponseRedirect(question.get_absolute_url())

