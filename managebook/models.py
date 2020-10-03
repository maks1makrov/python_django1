from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models import Avg


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
    cached_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self):
        return self.title if self.title is not None else "name not defined"


class Comment(models.Model):
    text = models.TextField(verbose_name="add a comment")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="comment")
    like = models.ManyToManyField(User, through="CommentLike", related_name="like", blank=True, null=True)
    cached_like = models.PositiveIntegerField(default=0)


class CommentLike(models.Model):
    class Meta:
        unique_together = ['comment', 'user']

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_like')

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            CommentLike.objects.get(comment_id=self.comment.id, user_id=self.user.id).delete()
        self.comment.cached_like = self.comment.comment_like.count()
        self.comment.save()


class BookLike(models.Model):
    class Meta:
        unique_together = ['user', 'book']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_like")
    rate = models.PositiveIntegerField(default=0)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except IntegrityError:
            bl = BookLike.objects.get(user=self.user, book=self.book)
            bl.rate = self.rate
            bl.save()
        else:
            self.book.cached_rate = self.book.book_like.aggregate(Avg('rate'))['rate__avg']
            self.book.save()
