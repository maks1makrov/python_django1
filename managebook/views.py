from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world")


def hello1(request):
    response = {"user": "Maks" }
    return render(request, 'index.html', response)




