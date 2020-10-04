from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, widgets, Textarea, TextInput, CharField
from django import forms

from managebook.models import Book, Comment


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ("title", "text", "genre")
        widgets = {
            'title': TextInput(attrs={'class': "form-control"}),
            "text": Textarea(attrs={'class': "form-control"})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            'text': TextInput(attrs={'class': "form-control"})
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        widgets = {
            'username': TextInput(attrs={'class': "form-control"})
        }

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': "form-control"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': "form-control"}),
        strip=False,

    )
