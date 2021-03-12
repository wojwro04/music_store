from django.contrib import admin

from .models import Question, Album, Artist, Track

admin.site.register(Question)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Track)
