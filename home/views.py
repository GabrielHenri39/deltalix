from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpRequest

# Create your views here.

def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page.
    """
    if request.method == "GET":
        return render(request, 'index.html')
    

def contato(request: HttpRequest) -> HttpResponse:
    """
    Render the contact page.
    """
    if request.method == "GET":
        return render(request, 'contato.html')