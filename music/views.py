from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()

# Create your views here.
from .models import Album
from .models import Track
from .models import Artist


def index(request):
    return HttpResponse("Witaj na stronie z muzyką.")

def albums(request):
    albums = Album.objects.all()
    lista = ""
    for album in albums:
        lista += album.title+ "<br>"
    return HttpResponse("Tutaj widoczne sa wszystkie albumy:<br> %s"% lista)

def tracks(request):
    tracks = Track.objects.all()
    lista = ""
    for track in tracks:
        lista += track.name + "<br>"
    return HttpResponse("Tutaj widoczne sa wszystkie utwory:<br> %s" % lista)

def artists(request):
    artists = Artist.objects.all()
    lista = ""
    for artist in artists:
        lista += artist.name + "<br>"
    return HttpResponse("Tutaj widoczne sa wszyscy artyści:<br> %s" % lista)

def add_artists(request):
    new_name = "Rolling Stones"
    q = Artist.objects.filter(name=new_name)
    if len(q) == 0:
        a = Artist(name=new_name)
        a.save()
        log = "Dodano artystę..."
    else:
        log = "Artysta już istnieje..."
    return HttpResponse(log)

def import_artists(request):
    cur.execute('SELECT * FROM artists')
    return cur.fetchall()
