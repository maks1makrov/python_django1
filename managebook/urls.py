from django.urls import path

from managebook import views

urlpatterns = [
    path('hello/', views.BookView.as_view(), name='hello'),
    path('hello1/', views.hello1, name='hello1111'),
    path("add_rate/<int:rate>/<int:book_id>", views.AddRateBook.as_view(), name="add_rate"),
    path("add_like/<int:comment_id>", views.AddLikeComment.as_view(), name="add_like"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("add_book/", views.AddNewBook.as_view(), name='add_book'),
    path("add_comment/<int:book_id>", views.AddComment.as_view(), name="add_comment"),
    path("delete_book/<int:book_id>", views.DeleteBook.as_view(), name="delete_book"),
    path("update_book/<str:book_slug>", views.UpdateBook.as_view(), name="update_book"),
]
