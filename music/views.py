from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import sqlite3


# Create your views here.
from .models import Album
from .models import Track
from .models import Artist


#def index(request):
#    return HttpResponse("Witaj na stronie z muzyką.")
def index(request):
    album_list = Album.objects.all()
    template = loader.get_template('music/index.html')
    context = {
        'album_list': album_list,
    }
    return HttpResponse(template.render(context, request))

def albums(request):
    albums = Album.objects.all()
    lista = ""
    for album in albums:
        title = album.title
        artist = album.album_artist()
        track_list = album.album_tracks()
        lista += f"{album.title} "
        lista += f"({artist}): "
        lista += f"{track_list}<br>"
    return HttpResponse("Tutaj widoczne sa wszystkie albumy:<br> %s"% lista)

def album(request, album_title):
    a = Album.objects.get(title=album_title)
    artist_name = a.album_artist()
    artist = Artist.objects.get(name=a.album_artist())
    #
    albums = Album.objects.filter(artist=artist)
    print(albums)
    #
    tracks = a.album_tracks()
    track_list = tracks.split(',')
    template = loader.get_template('music/album.html')
    context = {
        'album_title': album_title,
        'artist_name': artist_name,
        'track_list': track_list,
        'artist': artist,
    }
    return HttpResponse(template.render(context, request))

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

def artist(request, artist):
    a = Artist.objects.get(name=artist)
    template = loader.get_template('music/artist.html')
    context = {
        'artist': artist,
    }
    return HttpResponse(template.render(context, request))
    
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
    #Album.objects.all().delete()
    
    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM albums')
    albums = cur.fetchall()
    cur.execute('SELECT * FROM tracks')
    tracks = cur.fetchall()
    cur.execute('SELECT * FROM artists')
    artists = cur.fetchall()
    excepted = ""
    added = ""
    for album in albums:
        album_id = album[0]
        new_title = album[1]
        al_artist_id = album[2]
        q = Album.objects.filter(title=new_title)
        if len(q) == 0:
            a = Album(title=new_title)
            a.save()
            added += new_title + '<br>'
        else:
            excepted += new_title + '<br>'
        
        a = Album.objects.get(title=new_title)
        
        for track in tracks:
            tr_name = track[1]
            tr_album_id = track[2]
            if tr_album_id == album_id:
                tr = Track.objects.get(name=tr_name)
                a.track.add(tr)
                a.save()
        
        for artist in artists:
            artist_id = artist[0]
            ar_name = artist[1]
            if artist_id == al_artist_id:
                ar = Artist.objects.get(name=ar_name)
                a.artist = ar
                a.save()
                break
        
    return HttpResponse("Pominięto:<br> %s<br>Dodano:<br>%s" % (excepted,added))

# def import_tracks_to_albums(request):
    # con = sqlite3.connect('../chinook.db')
    # cur = con.cursor()
    # cur.execute('SELECT * FROM tracks')
    # rows = cur.fetchall()
    # added = ""
    # for row in rows:
        # track_id = row[0]
        # name = row[1]
        # q = Album.objects.filter(track=track_id)
        # if q:
            # Album.track.add(name)
            # added += f"Album: {Album.title}"
    # return HttpResponse("Zrobione<br>%s" % added)


# def import_tracks_to_albums2(request):
    # con = sqlite3.connect('../chinook.db')
    # cur = con.cursor()
    # added = ""
    # albums = Album.objects.all()
    # for a in albums:
        # print(a.title)
        # #if a.title !="Kult":
        # try:
            # cur.execute('SELECT AlbumId FROM albums WHERE Title = "{}"'.format(a.title))
            # rows = cur.fetchall()
            # albumid = rows[0][0]
            # cur.execute("SELECT Name FROM tracks WHERE AlbumId = '{}'".format(albumid))
            # rows = cur.fetchall()
            # for r in rows[0]:
                # tr = Track.objects.get(name=r)
                # a.track.add(tr)
                # #print("\t", tr)
                # a.save()
        # except:
            # pass


    # return HttpResponse("Zrobione<br>%s" % added)

