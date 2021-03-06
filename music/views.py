from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
import sqlite3


# Create your views here.
from .models import Album
from .models import Track
from .models import Artist
from .models import Genre
from .models import Playlist
from .forms import SearchForm

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if request.POST['choice_field'] == 'track':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return track(request, request.POST['title'])
                        except Track.DoesNotExist:
                            tracks = []
                            return search_results_tracks(request, tracks)
                    else:                
                        tracks = Track.objects.filter(name__contains=request.POST['title'])
                        return search_results_tracks(request, tracks)
            if request.POST['choice_field'] == 'artist':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return artist(request, request.POST['title'])
                        except Artist.DoesNotExist:
                            artists = []
                            return search_results_artists(request, artists)
                    else:                
                        artists = Artist.objects.filter(name__contains=request.POST['title'])
                        return search_results_artists(request, artists)
            if request.POST['choice_field'] == 'album':
                if request.POST['title']:
                    if 'exact' in request.POST:
                        try:
                            return album(request, request.POST['title'])
                        except Album.DoesNotExist:
                            albums = []
                            return search_results_albums(request, albums)
                    else:                
                        albums = Album.objects.filter(title__contains=request.POST['title'])
                        return search_results_albums(request, albums)
    else:
        form = SearchForm()
    template = loader.get_template('music/search.html')
    return HttpResponse(template.render({'form': form}, request))

def search_results_tracks(request, tracks):
    template = loader.get_template('music/search_results_tracks.html')
    context = {
        'tracks': tracks,
    }
    return HttpResponse(template.render(context, request))

def search_results_artists(request, artists):
    template = loader.get_template('music/search_results_artists.html')
    context = {
        'artists': artists,
    }
    return HttpResponse(template.render(context, request))

def search_results_albums(request, albums):
    template = loader.get_template('music/search_results_albums.html')
    context = {
        'albums': albums,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('music/index.html')
    return HttpResponse(template.render({}, request))

def artists(request):
    artists = Artist.objects.all()
    template = loader.get_template('music/artists.html')
    context = {
        'artists': artists,
    }
    return HttpResponse(template.render(context, request))

def artist(request, artist):
    a = Artist.objects.get(name=artist)
    album_list = Album.objects.filter(artist=a)
    template = loader.get_template('music/artist.html')
    context = {
        'artist': artist,
        'album_list': album_list,
    }
    return HttpResponse(template.render(context, request))

def genres(request):
    genres = Genre.objects.all()
    template = loader.get_template('music/genres.html')
    context = {
        'genres': genres,
    }
    return HttpResponse(template.render(context, request))

def genre(request, genre):
    g = Genre.objects.get(name=genre)
    track_list = Track.objects.filter(genre=g)
    template = loader.get_template('music/genre.html')
    context = {
        'genre': genre,
        'track_list': track_list,
    }
    return HttpResponse(template.render(context, request))

def tracks(request):
    tracks = Track.objects.all()
    lista = ""
    for track in tracks:
        lista += track.name + "<br>"
    return HttpResponse("Tutaj widoczne sa wszystkie utwory:<br> %s" % lista)

def track(request, track_name):
    t = Track.objects.get(name=track_name)
    albums = Album.objects.filter(track=t)
    genre = t.genre
    template = loader.get_template('music/track.html')
    context = {
        'track_name': track_name,
        'albums': albums,
        'genre': genre,
    }
    return HttpResponse(template.render(context, request))

def albums(request):
    albums = Album.objects.all()
    template = loader.get_template('music/albums.html')
    context = {
        'albums': albums,
    }
    return HttpResponse(template.render(context, request))

def album(request, album_title):
    a = Album.objects.get(title=album_title)
    artist = Artist.objects.get(name=a.album_artist())
    track_list = a.track.all()
    template = loader.get_template('music/album.html')
    context = {
        'album_title': album_title,
        'track_list': track_list,
        'artist': artist,
    }
    return HttpResponse(template.render(context, request))

def playlists(request):
    playlists = Playlist.objects.all()
    template = loader.get_template('music/playlists.html')
    context = {
        'playlists': playlists,
    }
    return HttpResponse(template.render(context, request))

def playlist(request, playlist_name):
    p = Playlist.objects.get(name=playlist_name)
    track_list = p.track.all()
    template = loader.get_template('music/playlist.html')
    context = {
        'playlist_name': playlist_name,
        'track_list': track_list,
    }
    return HttpResponse(template.render(context, request))

def add_artists(request):
    new_name = "Rolling Stones"
    q = Artist.objects.filter(name=new_name)
    if len(q) == 0:
        a = Artist(name=new_name)
        a.save()
        log = "Dodano artyst??..."
    else:
        log = "Artysta ju?? istnieje..."
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
    return HttpResponse("Pomini??to:<br> %s<br>Dodano:<br>%s" % (excepted,added))

def import_genres(request):
    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM genres')
    rows = cur.fetchall()
    excepted = ""
    added = ""
    for row in rows:
        new_name = row[1]
        q = Genre.objects.filter(name=new_name)
        if len(q) == 0:
            g = Genre(name=new_name)
            g.save()
            added += new_name + '<br>'
        else:
            excepted += new_name + '<br>'
    return HttpResponse("Pomini??to:<br> %s<br>Dodano:<br>%s" % (excepted,added))

def import_tracks(request):
    #Track.objects.all().delete()
    
    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM tracks')
    tracks = cur.fetchall()
    cur.execute('SELECT * FROM genres')
    genres = cur.fetchall()
    excepted = ""
    added = ""
    for track in tracks:
        new_name = track[1]
        tr_genre_id = track[4]
        new_composer = track[5]
        new_miliseconds = track[6]
        new_bytes = track[7]
        new_unit_price = track[8]
        q = Track.objects.filter(name=new_name)
        if len(q) == 0:
            t = Track(name=new_name, composer=new_composer, miliseconds=new_miliseconds, bytes=new_bytes, unit_price=new_unit_price)
            t.save()
            added += f"{new_name}, {new_composer}, {new_miliseconds}, {new_bytes}, {new_unit_price}'<br>'"
        else:
            excepted += f"{new_name}, {new_composer}, {new_miliseconds}, {new_bytes}, {new_unit_price}'<br>'"
        
        t = Track.objects.get(name=new_name)
        
        for genre in genres:
            genre_id = genre[0]
            g_name = genre[1]
            if genre_id == tr_genre_id:
                g = Genre.objects.get(name=g_name)
                t.genre = g
                t.save()
                break
                
    return HttpResponse("Pomini??to:<br> %s<br>Dodano:<br>%s" % (excepted,added))

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
        
    return HttpResponse("Pomini??to:<br> %s<br>Dodano:<br>%s" % (excepted,added))

def import_playlists(request):
    #Playlist.objects.all().delete()
    
    con = sqlite3.connect('../chinook.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM playlists')
    playlists = cur.fetchall()
    cur.execute('SELECT * FROM playlist_track')
    playlist_tracks = cur.fetchall()
    cur.execute('SELECT * FROM tracks')
    tracks = cur.fetchall()
    excepted = ""
    added = ""
    for playlist in playlists:
        playlist_id = playlist[0]
        new_name = playlist[1]
        q = Playlist.objects.filter(name=new_name)
        if len(q) == 0:
            p = Playlist(name=new_name)
            p.save()
            added += new_name + '<br>'
        else:
            excepted += new_name + '<br>'
        
        p = Playlist.objects.get(name=new_name)
        
        for playlist_track in playlist_tracks:
            pltr_playlist_id = playlist_track[0]
            pltr_track_id = playlist_track[1]
            if pltr_playlist_id == playlist_id:
                for track in tracks:
                    track_id = track[0]
                    track_name = track[1]
                    if track_id == pltr_track_id:
                        tr = Track.objects.get(name=track_name)
                        p.track.add(tr)
                        p.save()

    return HttpResponse("Pomini??to:<br> %s<br>Dodano:<br>%s" % (excepted,added))

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

