from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    content = models.TextField(blank=False, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('question_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=False, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)


