from django.db.models import Avg
from django.test import TestCase
from django.urls import reverse

from managebook.models import BookLike, Book, Comment, Genre
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
    def setUp(self): # метод который запускается каждый раз когда запускаеься тест
        self.user = User.objects.create_user(username="test Name", password='test pwd')
        self.client.force_login(self.user)

    def test_hello(self):
        url = reverse('hello')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_rate(self):
        book = Book.objects.create(text="text", slug='slug')
        url = reverse('add_rate', args=[7, book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.cached_rate, 7)
        self.client.logout()
        url = reverse('add_rate', args=[1, book.id])
        response = self.client.get(url)
        book.refresh_from_db()
        self.assertEqual(book.cached_rate, 7)


    def test_add_like(self):
        book = Book.objects.create(text="text", slug='slug')
        comment = Comment.objects.create(text="text", user=self.user, book=book)
        url = reverse('add_like', args=[comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        comment.refresh_from_db()
        self.assertEqual(comment.cached_like, 1)

    def test_add_comment(self):
        book = Book.objects.create(text="text", slug='slug')
        data = {"text": "text for comment"}
        url = reverse('add_comment', args=[book.id])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.comment.first().text, data['text'])



    def test_delete_book(self):
        book = Book.objects.create(text='text', slug="slug")
        book.author.add(self.user)
        book.save()
        url = reverse('delete_book', args=[book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.count(), 0)


    def test_update_book(self):
        g1 = Genre.objects.create(title="genre1")
        g2 = Genre.objects.create(title="genre2")
        book = Book.objects.create(text='text', slug="slug")
        book.author.add(self.user)
        book.genre.add(g1)
        book.save()
        url = reverse('update_book', args=[book.slug])
        data = {"title": "text title", "text": 'text text', "genre": ["2"]}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.genre.first().title, g2.title)


    def test_login(self):
        self.client.logout()
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        data = {"username": 'test Name',
                'password': "test pwd"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)


    def test_add_book(self):
        g1 = Genre.objects.create(title="genre1")
        data = {"title": "text title",
                "text": 'text text', "genre": ["1"]}
        url = reverse('add_book')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        book = Book.objects.first()
        self.assertEqual(book.title, data['title'])

    def test_delete_comment(self):
        book = Book.objects.create(text='text', slug="slug")
        comment = Comment.objects.create(text="text", user=self.user, book=book)
        url = reverse('delete_comment', args=[comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
