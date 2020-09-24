from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Book(models.Model):
    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

    title = models.CharField(max_length=50,
                             verbose_name="название",
                             help_text="enter name of book",
                             db_index=True)
    slug = models.SlugField(unique=True)
    text = models.TextField(unique=True)
    author = models.ManyToManyField(User)
    publish_date = models.DateField(auto_now_add=True)
    genre = models.ManyToManyField("managebook.Genre")
    rate = models.ManyToManyField(User, through="managebook.BookLike", related_name="rate")

    def __str__(self):
        return self.title if self.title is not None else "name not defined"


class Comment(models.Model):
    text = models.TextField(verbose_name="text")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name="like")


class BookLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)
