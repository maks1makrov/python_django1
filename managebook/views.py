from datetime import datetime
from pickle import GET

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Q, CharField, Value, OuterRef, Subquery, Exists, Prefetch
from django.db.models.functions import Cast
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from pytils.translit import slugify

from managebook.forms import BookForm, CommentForm, CustomUserCreationForm, CustomAuthenticationForm
from managebook.models import BookLike, Book, CommentLike, Comment
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



# class BookView(View):
#     # @method_decorator(cache_page(5))
#     def get(self, request):
#         response = {}
#         if request.user.is_authenticated:
#             quary = Q(book_like__user_id=request.user.id)
#             sub_quary = Book.objects.filter(quary). \
#                 annotate(user_rate=Cast('book_like__rate', CharField())). \
#                 prefetch_related("author", "genre", "comment", "comment__user")
#             result = Book.objects.filter(~quary).annotate(user_rate=Value(-1, CharField())). \
#                 prefetch_related("author", "genre", "comment", "comment__user").union(sub_quary)
#             response['content'] = result.all()
#         else:
#             response['content'] = Book.objects. \
#                 prefetch_related("author", "genre", "comment", "comment__user").all()
#         response['form'] = CommentForm()
#         return render(request, "index.html", response)


class BookView(View):
    # @method_decorator(cache_page(5))
    def get(self, request, num_page=1):
        response = {}
        if request.user.is_authenticated:
            sub_query_1 = BookLike.objects.filter(user=request.user, book=OuterRef('pk')).values('rate')
            sub_query_2 = Exists(User.objects.filter(id=request.user.id, book=OuterRef('pk')))
            sub_query_3 = Exists(User.objects.filter(id=request.user.id, comment=OuterRef('pk')))
            sub_query_4 = Exists(User.objects.filter(id=request.user.id, like=OuterRef('pk')))
            comment = Comment.objects.annotate(is_owner=sub_query_3, is_liked=sub_query_4).\
                select_related('user').prefetch_related('like')
            comment_prefetch = Prefetch('comment', comment)
            result = Book.objects.annotate(user_rate=Cast(sub_query_1, CharField()), is_owner=sub_query_2).\
                prefetch_related(comment_prefetch, "author", "genre", 'rate')

        else:
            result = Book.objects. \
                prefetch_related("author", "genre", "comment", "comment__user").all()
        response['form'] = CommentForm()
        pag = Paginator(result, 3)
        response['content'] = pag.page(num_page)
        response['count_page'] = list(range(1, pag.num_pages + 1))
        response['bookform'] = BookForm()
        return render(request, "index.html", response)


# class BookView(View):
#     def get(self, request):
#         if request.user.username in cache:
#             result = cache.get(request.user.username)
#             response = {"content": result, "form": CommentForm()}
#             return render(request, "index.html", response)
#         response = {}
#         if request.user.is_authenticated:
#             quary = Q(book_like__user_id=request.user.id)
#             sub_quary = Book.objects.filter(quary). \
#                 annotate(user_rate=Cast('book_like__rate', CharField())). \
#                 prefetch_related("author", "genre", "comment", "comment__user")
#             result = Book.objects.filter(~quary).annotate(user_rate=Value(-1, CharField())). \
#                 prefetch_related("author", "genre", "comment", "comment__user").union(sub_quary)
#             response['content'] = result.all()
#         else:
#             response['content'] = Book.objects. \
#                 prefetch_related("author", "genre", "comment", "comment__user").all()
#         response['form'] = CommentForm()
#         cache.set(request.user.username, result, 10)
#         return render(request, "index.html", response)


class AddComment(View):
    def post(self, request, book_id):
        if request.user.is_authenticated:
            new_comment = CommentForm(request.POST)
            if new_comment.is_valid():
                nc = new_comment.save(commit=False)
                nc.user = request.user
                nc.book_id = book_id
                nc.save()
        return redirect("hello")

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


class DeleteComment(View):
    def get(self, request, comment_id):
        if request.user.is_authenticated:
            try:
                Comment.objects.get(id=comment_id, user=request.user).delete()
            except Comment.DoesNotExist:
                pass
        return redirect("hello")

class UpdateComment(View):
    def get(self, request, comment_id):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=comment_id)
            if request.user == comment.user:
                form = CommentForm(instance=comment)
                return render(request, "update_comment.html", {"form": form, "comment_id": comment_id})
        return redirect("hello")

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            comment.save()
            return redirect("hello")
        form = CommentForm(instance=comment)
        return render(request, "update_comment.html", {"form": form, "comment_id": comment_id})

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        messages.error(request, "error")
        return redirect("register")

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = CustomAuthenticationForm(data=request.POST)
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


class DeleteBook(View):
    def get(self, request, book_id):
        if request.user.is_authenticated:
            book = Book.objects.get(id=book_id)
            if request.user in book.author.all():
                book.delete()
            return redirect("hello")


class UpdateBook(View):
    def get(self, request, book_slug):
        if request.user.is_authenticated:
            book = Book.objects.get(slug=book_slug)
            if request.user in book.author.all():
                df = BookForm(instance=book)
                return render(request, 'update_book.html', {"form": df, "slug": book.slug})
            return redirect("hello")

    def post(self, request, book_slug):
        book = Book.objects.get(slug=book_slug)
        bf = BookForm(instance=book, data=request.POST)
        if bf.is_valid():
            bf.save()
        return redirect("hello")


class AddLikeAjax(View):
    def post(self, request):
        if request.user.is_authenticated:
            cl_id = request.POST['cl_id'][3:]
            flag = CommentLike(user=request.user, comment_id=cl_id).save()
            comment = Comment.objects.get(id=cl_id)
            return JsonResponse({"ok": True,
                                 'count_like': comment.cached_like,
                                 'flag': flag,
                                 'user': request.user.username
                                 })
        return JsonResponse({"ok": False})


class AddRateAjax(View):
    def post(self, request):
        if request.user.is_authenticated:
            book_id = request.POST['book_id']
            rate = request.POST['book_rate']
            bl = BookLike(user=request.user, book_id=book_id, rate=rate)
            flag = bl.save()
            bl.book.refresh_from_db()
            return JsonResponse({'user': request.user.username, "flag": flag, 'cached_rate': bl.book.cached_rate, 'rate': bl.rate })
        return JsonResponse({"ok": False})


class DeleteCommentAjax(View):
    def delete(self, request, comment_id):
        if request.user.is_authenticated:
            Comment.objects.filter(id=comment_id, user=request.user).delete()
        return JsonResponse({"ok": False})


class AddNewBookAjax(View):
    def post(self):
        pass