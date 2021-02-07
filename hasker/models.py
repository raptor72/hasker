from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    content = models.TextField(blank=False, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='questions')
    date_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('question_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('question_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('question_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def answer_count(self):
        return self.answer_set.values().__len__()

    def user_can_vote(self, user):
        query_set = user.vote_set.all().filter(question=self)
        if query_set.exists():
            return False
        return True

    class Meta:
        ordering = ['-date_create']


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    def vote_count(self):
        return self.vote_set.values().__len__()


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)