from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import *
from django.views.generic import View
from .utils import *
from django.urls import reverse
from django.views import generic
from .forms import TagForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q


class IndexView(generic.ListView):
    template_name='hasker/index.html'
    context_object_name='questions'
    paginate_by = 2
#    queryset = Question.objects.all()

#    def get_queryset(self):
#        return Question.objects.all()

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Question.objects.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        return Question.objects.all()


def tags_list(request):
#    search_query = request.GET.get('search', '')
#
#    if search_query:
#        tags = Tag.objects.filter(title__icontains=search_query)
#    else:
#        tags = Tag.objects.all()

    tags = Tag.objects.all()
    paginator = Paginator(tags, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }

    return render(request, 'hasker/tags_list.html', context=context)


class QuestionDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Question
    redirect_url = 'accounts:login'
    template = 'hasker/question_detail.html'


class TagDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Tag
    redirect_url = 'accounts:login'
    template = 'hasker/tag_detail.html'

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model  = TagForm
    template = 'hasker/tag_create.html'

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
    form_model  = QuestionForm
    template = 'hasker/question_create.html'

class QuestionUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Question
    model_form = QuestionForm
    template = 'hasker/question_update_form.html'

class QuestionDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Question
    template = 'hasker/question_delete_form.html'
    redirect_url = 'questions_list_url'

