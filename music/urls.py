from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('albums', views.albums, name='albums'),
    path('tracks', views.tracks, name='tracks'),
    path('artists', views.artists, name='artists'),
    path('add_artists', views.add_artists, name='add_artists'),
    path('import_artists', views.import_artists, name='import_artists'),
    path('import_tracks', views.import_tracks, name='import_tracks'),
    path('import_albums', views.import_albums, name='import_albums'),
]
