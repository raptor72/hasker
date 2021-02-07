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


class IndexView(generic.ListView):
    template_name='hasker/index.html'
    context_object_name='questions'
    paginate_by = 8
#    queryset = Question.objects.all()

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Question.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        return Question.objects.all()


def tags_list(request):
    tags = Tag.objects.all()
    paginator = Paginator(tags, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    is_paginated = page_obj.has_other_pages()

    context = {
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'page_obj.paginator': paginator,
    }

    return render(request, 'hasker/tags_list.html', context=context)


# class QuestionDetail(LoginRequiredMixin, ObjectDetailMixin, View):
#     model = Question
#     form_model = AnswerForm
#     redirect_url = 'accounts:login'
#     template = 'hasker/question_detail.html'


def question_detail(request, slug):
    user = request.user
    question = get_object_or_404(Question, slug=slug)
    if request.method == 'POST' and user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            Answer.objects.create(question=question, content=text, user=user)
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        if question.author == user:
            return render(request, 'hasker/question_detail.html', context={'question': question,})
        form = AnswerForm()
        user_can_vote = question.user_can_vote(request.user)
        if user_can_vote:
            return render(request, 'hasker/question_detail.html', context={'form': form, 'question': question, 'user_can_vote': user_can_vote})
        else:
            choised_answer_id = question.vote_set.filter(user=user).first().answer.id
            return render(request, 'hasker/question_detail.html',
                          context={'form': form, 'question': question, 'choised_answer_id': choised_answer_id})


class TagDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Tag
    redirect_url = 'accounts:login'
    template = 'hasker/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'hasker/tag_create.html'


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'hasker/tag_update_form.html'

#    def get(self, request, slug):
#        tag = Tag.objects.get(slug__iexact=slug)
#        bound_form = TagForm(instance=tag)
#        return render(request, 'hasker/tag_update_form.html', context={'form': bound_form, 'tag':tag})

#    def post(self, request, slug):
#        tag = Tag.objects.get(slug__iexact=slug)
#        bound_form = TagForm(request.POST, instance=tag)

#        if bound_form.is_valid():
#            new_tag = bound_form.save()
#            return redirect(new_tag)
#        return render(request, 'hasker/tag_update.html', context={'form': bound_form, 'tag':tag})


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'hasker/tag_delete_form.html'
    redirect_url = 'tags_list_url'

    # def get(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     return render(request, 'hasker/tag_delete_form.html', context={'tag': tag})
    #
    # def post(self, request, slug):
    #     tag = Tag.objects.get(slug__iexact=slug)
    #     tag.delete()
    #     return redirect(reverse('tags_list_url'))


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
    answer = Answer.objects.get(id=answer_id)
    question = answer.question
    # question = get_object_or_404(Answer, question=answer)
    user_can_vote = question.user_can_vote(user)
    if request.method == 'GET' and user.is_authenticated:
        if user_can_vote:
            Vote.objects.create(question=question, user=user, answer=answer)
        else:
            vote = Vote.objects.filter(question=question, user=user).first()
            vote.delete()
    return HttpResponseRedirect(question.get_absolute_url())



