from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('albums', views.albums, name='albums'),
    path('album/<str:album_title>/', views.album, name='album'),
    path('tracks', views.tracks, name='tracks'),
    path('artists', views.artists, name='artists'),
    path('playlists', views.playlists, name='playlists'),
    path('genre/<str:genre>/', views.genre, name='genre'),
    path('playlist/<str:playlist_name>/', views.playlist, name='playlist'),
    path('genres', views.genres, name='genres'),
    path('artist/<str:artist>/', views.artist, name='artist'),
    path('track/<str:track_name>/', views.track, name='track'),
    path('add_artists', views.add_artists, name='add_artists'),
    path('import_artists', views.import_artists, name='import_artists'),
    path('import_genres', views.import_genres, name='import_genres'),
    path('import_tracks', views.import_tracks, name='import_tracks'),
    path('import_albums', views.import_albums, name='import_albums'),
    path('import_playlists', views.import_playlists, name='import_playlists'),
    # path('import_tracks_to_albums', views.import_tracks_to_albums, name='import_tracks_to_albums'),
    # path('import_tracks_to_albums2', views.import_tracks_to_albums2, name='import_tracks_to_albums2'),
]
