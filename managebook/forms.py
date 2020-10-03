from django.forms import ModelForm, widgets, Textarea, TextInput

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