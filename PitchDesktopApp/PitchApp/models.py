from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    artist_name = models.CharField(verbose_name="Artist Name", max_length=250)
    country = CountryField()

    # class Meta:
    # unique_together = ["user", "artist_name"]


class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_type = models.CharField(verbose_name="Type of Account", max_length=50)
    country = CountryField()
    age = models.IntegerField(verbose_name="Age", null=True)
    card = models.CharField(verbose_name="Card Number", max_length=19)


class Subscription(models.Model):
    user_id = models.OneToOneField(NormalUser, on_delete=models.CASCADE)
    due_date = models.DateField(verbose_name="Due Date")


class Playlist(models.Model):
    user_id = models.OneToOneField(NormalUser, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Title of the playlist", max_length=100)


class Creates(models.Model):
    user_id = models.OneToOneField(NormalUser, on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class Album(models.Model):
    title = models.CharField(
        verbose_name="Album Title", max_length=250, default="Single"
    )
    year = models.PositiveIntegerField(
        verbose_name="Year of Release",
        default=datetime.date.today().year,
        validators=[
            MinValueValidator(1857),
            MaxValueValidator(datetime.date.today().year),
        ],
    )
    cover_file = models.ImageField(verbose_name="Album Cover")
    artist = models.ForeignKey(
        Artist,
        verbose_name="Name of the Artist",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Audio(models.Model):
    # playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name="Audio Title", max_length=100)
    duration = models.DurationField(verbose_name="Duration")
    times_played = models.PositiveIntegerField(
        verbose_name="No. of times played", validators=[MinValueValidator(0)]
    )
    audio_file = models.FileField(verbose_name="Audio File")

    def __str__(self):
        return self.title


class Features(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    audio_id = models.ForeignKey(Audio, on_delete=models.CASCADE)


class Song(models.Model):
    audio_id = models.ForeignKey(Audio, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)


class Tag(models.Model):
    audio_id = models.ForeignKey(Audio, on_delete=models.CASCADE)
    tag1 = models.CharField(verbose_name="Tag 1", max_length=12)
    tag2 = models.CharField(verbose_name="Tag 2", max_length=12)
    tag3 = models.CharField(verbose_name="Tag 3", max_length=12)


class Podcast(models.Model):
    audio_id = models.ForeignKey(Audio, on_delete=models.CASCADE)
