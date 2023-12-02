from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = News
        fields = ['title', 'slug', 'content', 'photo', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError('Длина превышает 200 символов')
 
        return title

class AddCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ['comment', ]
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 600:
            raise forms.ValidationError('Длина превышает 600 символов')
        return comment