from django import forms
from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "status"]
        labels = {"title": "Заголовок", "body": "Текст", "status": "Статус"}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": "Комментарий"}
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}
