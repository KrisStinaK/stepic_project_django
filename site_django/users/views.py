from django.shortcuts import render, HttpResponse


def login_user(request):
    return HttpResponse('<h1>login</h1>')


def logout_user(request):
    return HttpResponse('<h1>logout</h1>')
