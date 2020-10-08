from django.db.models import Avg
from django.test import TestCase
from django.urls import reverse

from managebook.models import BookLike, Book, Comment
from django.contrib.auth.models import User


class TestModel(TestCase):
    def test_hello(self):
        print('hello')

    def test_rate(self):
        user_1 = User.objects.create(username="user_1")
        user_2 = User.objects.create(username="user_2")
        book = Book.objects.create(text="text", slug='slug')
        BookLike.objects.create(book=book, user=user_1, rate=4)
        BookLike.objects.create(book=book, user=user_2, rate=6)
        rate_avg = book.book_like.aggregate(Avg('rate'))['rate__avg']
        self.assertEqual(rate_avg, 5)

    def test_cached_rate(self):
        user_1 = User.objects.create(username="user_1")
        user_2 = User.objects.create(username="user_2")
        book = Book.objects.create(text="text", slug='slug')
        BookLike.objects.create(book=book, user=user_1, rate=4)
        BookLike.objects.create(book=book, user=user_2, rate=6)
        self.assertEqual(book.cached_rate, 5)


    def test_comment_like(self):
        user_1 = User.objects.create(username="user_1")
        user_2 = User.objects.create(username="user_2")
        book = Book.objects.create(text="text", slug='slug')
        comment = Comment.objects.create(text="text", user=user_1, book=book)
        comment.like.add(user_2)
        comment.like.add(user_1)
        comment.save()
        like = comment.like.count()
        self.assertEqual(like, 2)


class TestViews(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test Name", password='test pwd')
        self.client.force_login(user)

    def test(self):
        url = reverse('hello')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        book = Book.objects.create(text='text', slug="slug")
        url = reverse('delete_book', args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)