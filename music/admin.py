from django.contrib import admin

from .models import Question, Album, Artist, Track, Genre, Playlist

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Track)
admin.site.register(Album)
admin.site.register(Playlist)