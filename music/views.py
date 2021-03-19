from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import Album


def index(request):
    return HttpResponse("Witaj na stronie z muzyką.")

def albums(request):
    albums = Album.objects.all()
    lista = ""
    for album in albums:
        lista += album.title+ "<br>"
    return HttpResponse("Tutaj widoczne sa wszystkie albumy:<br> %s"% lista)
