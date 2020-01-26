from django import forms
from .models import Tag, Question
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
        return new_slug


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
#        fields = ['author', 'title', 'slug', 'content', 'tags']
#        fields = ['title', 'slug', 'content', 'tags']
        fields = ['title', 'content', 'tags']
        widgets = {
#            'author': forms.ModelChoiceField(queryset=Question.objects),
#            'author': forms.SelectMultiple(attrs={'class': 'form-control'}),
#            'author': forms.ChoiceField(choices=User.objects.all()),
#            'author': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
#            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        return new_slug

