from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
        
class Track(models.Model):
    name = models.CharField(max_length=200)
    composer = models.CharField(max_length=200, null=True)
    miliseconds = models.PositiveIntegerField()
    bytes = models.PositiveIntegerField()
    unit_price = models.FloatField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)
    track = models.ManyToManyField(Track)

    def __str__(self):
        return self.title
        
    def album_artist(self):
        return self.artist
    
    def album_tracks(self):
        return ', '.join([a.name for a in self.track.all()])

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    track = models.ManyToManyField(Track)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
