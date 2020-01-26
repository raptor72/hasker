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

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})
