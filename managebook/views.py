from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count, Q, CharField, Value
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pytils.translit import slugify

from managebook.forms import BookForm, CommentForm
from managebook.models import BookLike, Book, CommentLike, Comment
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class BookView(View):
    def get(self, request):
        response = {}
        if request.user.is_authenticated:
            quary = Q(book_like__user_id=request.user.id)
            sub_quary = Book.objects.filter(quary). \
                annotate(user_rate=Cast('book_like__rate', CharField())). \
                prefetch_related("author", "genre", "comment", "comment__user")
            result = Book.objects.filter(~quary).annotate(user_rate=Value(-1, CharField())). \
                prefetch_related("author", "genre", "comment", "comment__user").union(sub_quary)
            response['content'] = result.all()
        else:
            response['content'] = Book.objects. \
                prefetch_related("author", "genre", "comment", "comment__user").all()
        response['form'] = CommentForm()
        return render(request, "index.html", response)


class AddComment(View):
    def post(self, request, book_id):
        new_comment = CommentForm(request.POST)
        if new_comment.is_valid():
            nc = new_comment.save(commit=False)
            nc.user = request.user
            nc.book = Book.objects.get(id=book_id)
            nc.save()
        response = {}
        if request.user.is_authenticated:
            quary = Q(book_like__user_id=request.user.id)
            sub_quary = Book.objects.filter(quary). \
                annotate(user_rate=Cast('book_like__rate', CharField())). \
                prefetch_related("author", "genre", "comment", "comment__user")
            result = Book.objects.filter(~quary).annotate(user_rate=Value(-1, CharField())). \
                prefetch_related("author", "genre", "comment", "comment__user").union(sub_quary)
            response['content'] = result.all()
        else:
            response['content'] = Book.objects. \
                prefetch_related("author", "genre", "comment", "comment__user").all()
        return render(request, "index.html", response)

# def hello(request):
#     return HttpResponse("Hello world")


def hello1(request):
    response = {"user": "Maks"}
    return render(request, 'index.html', response)


class AddRateBook(View):
    def get(self, request, rate, book_id):
        if request.user.is_authenticated:
            BookLike.objects.create(book_id=book_id, rate=rate, user_id=request.user.id)
        return redirect("hello")

class AddLikeComment(View):
    def get(self, request, comment_id):
        if request.user.is_authenticated:
            CommentLike.objects.create(comment_id=comment_id, user_id=request.user.id)
        return redirect("hello")


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hello')
        messages.error(request, "error")
        return redirect("register")

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('hello')
        messages.error(request, message="login or password is not correct")
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('hello')


class AddNewBook(View):
    def get(self, request):
        form = BookForm()
        return render(request, "create_book.html", {"form": form})

    def post(self, request):
        book = BookForm(data=request.POST)
        if book.is_valid():
            nb = book.save(commit=False)
            nb.slug = slugify(nb.title)
            try:
                nb.save()
            except IntegrityError:
                nb.slug += datetime.now().strftime("%Y:%m:%d:%H:%M:%S:%f")
                nb.save()
            nb.author.add(request.user)
            book.save_m2m()
            return redirect('hello')
        return redirect('add_book')

