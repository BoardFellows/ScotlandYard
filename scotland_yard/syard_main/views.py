# from django.shortcuts import render
from django.http import HttpResponse


def home_view(request, *args, **kwargs):
    welcome = "Welcome GameFellows!"
    return HttpResponse(welcome)
