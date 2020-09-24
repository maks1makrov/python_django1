from django.urls import path

from managebook import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('hello1/', views.hello1, name='hello1111')
]
