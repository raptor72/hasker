import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import *
from django.core.paginator import Paginator

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from hasker.models import Question, Answer


class ObjectDetailMixin:
    model = None
    template = None
    form_model = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'admin_object': obj,
                                                       'detail': True})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.form_model(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.user = request.user
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj,
                                                       'admin_object': obj, 'detail': True})


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.author = request.user
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower():obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


def fbv_paginator(request: WSGIRequest, queryset: QuerySet, paginate_by: int, page_string: str) -> dict:
    """
    Universal function based views paginator
    Return context dict with pagination objects
    """

    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get(page_string, 1)
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    context = {
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'page_obj.paginator': paginator,
    }

    return context


def count_answer_rating(answer):
    if not isinstance(answer, Answer):
        return
    rating = 0
    if answer.is_correct is True:
        rating += 5
    rating += answer.vote_count()
    answer.rating = rating
    answer.save()
    return rating


def recalculate_answers():
    recalculated_count = 0
    for answer in Answer.objects.all():
        rating = count_answer_rating(answer)
        logging.warning('counted rating {} fro answer {}'.format(str(rating), answer.content[0:20]))
        recalculated_count += 1
    return recalculated_count


def count_question_rating(question):
    if not isinstance(question, Question):
        return
    rating = 0
    rating += question.answer_count()
    for answer in question.answer_set.all():
        rating += answer.vote_count()
    question.rating = rating
    question.save()
    return rating


def recalculate_question():
    recalculated_count = 0
    for question in Question.objects.all():
        rating = count_question_rating(question)
        logging.warning('counted rating {} for question {}'.format(str(rating), question.content[0:20]))
        recalculated_count += 1
    return recalculated_count