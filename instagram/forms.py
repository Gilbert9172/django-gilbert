from django import forms
from django.forms import widgets

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["photo", "caption", "location"]

        # Model의 필드 속성을 수정해줄수 있다.
        widgets = {
            "caption":forms.Textarea,
        }