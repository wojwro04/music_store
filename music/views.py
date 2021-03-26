from django.shortcuts import render
from django.http import HttpResponse
import sqlite3


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
    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM artists')
    rows = cur.fetchall()
    excepted = ""
    added = ""
    for row in rows:
        new_name = row[1]
        q = Artist.objects.filter(name=new_name)
        if len(q) == 0:
            a = Artist(name=new_name)
            a.save()
            added += new_name + '<br>'
        else:
            excepted += new_name + '<br>'
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (excepted,added))

def import_tracks(request):

    Track.objects.all().delete()


    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM tracks')
    rows = cur.fetchall()
    excepted = ""
    added = ""
    for row in rows:
        new_name = row[1]
        new_composer = row[5]
        new_miliseconds = row[6]
        new_bytes = row[7]
        new_unit_price = row[8]
        q = Track.objects.filter(name=new_name)
        if len(q) == 0:
            t = Track(name=new_name, composer=new_composer, miliseconds=new_miliseconds, bytes=new_bytes, unit_price=new_unit_price)
            t.save()
            added += f"{new_name}, {new_composer}, {new_miliseconds}, {new_bytes}, {new_unit_price}'<br>'"
        else:
            excepted += f"{new_name}, {new_composer}, {new_miliseconds}, {new_bytes}, {new_unit_price}'<br>'"
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (excepted,added))

def import_albums(request):
    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM albums')
    rows = cur.fetchall()
    excepted = ""
    added = ""
    for row in rows:
        new_title = row[1]
        q = Album.objects.filter(title=new_title)
        if len(q) == 0:
            a = Album(title=new_title)
            a.save()
            added += new_title + '<br>'
        else:
            excepted += new_title + '<br>'
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (excepted,added))
