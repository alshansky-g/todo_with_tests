from django.shortcuts import render
from django.http import HttpRequest


def home_page(request: HttpRequest):
    return render(request, "home.html")
