from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Witaj na stronie z muzyką.")

def albums(request):
    return HttpResponse("Tutaj widoczne sa wszystkie albumy")