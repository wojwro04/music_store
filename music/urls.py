from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('albums', views.albums, name='albums'),
    path('tracks', views.tracks, name='tracks'),
    path('artists', views.artists, name='artists'),
    path('add_artists', views.add_artists, name='add_artists'),
]
