from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.forms import UserCreationForm
from .models import User, Artist, NormalUser, Album, Audio, Song
from django.db import transaction
from django_countries.fields import CountryField


class ArtistSignUpForm(UserCreationForm):
    artist_name = forms.CharField(max_length=250, required=True)
    country = CountryField().formfield()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2", "email"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_artist = True
        user.save()
        artist = Artist.objects.create(user=user)
        artist.artist_name = self.cleaned_data.get("artist_name")
        artist.country = self.cleaned_data.get("country")
        artist.save()
        return user


class NormalUserSignUpForm(UserCreationForm):
    country = CountryField().formfield()
    age = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2", "email"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        normal_user = NormalUser.objects.create(user=user)
        normal_user.country = self.cleaned_data.get("country")
        normal_user.age = self.cleaned_data.get("age")
        normal_user.save()
        return user


class AlbumUploadForm(ModelForm):
    class Meta:
        model = Album
        exclude = ["artist"]


<<<<<<< HEAD
class SongUploadForm(Form):
    pass
=======
class AudioForm(ModelForm):
    class Meta:
        model = Audio
        fields = "__all__"


class SongUploadForm(ModelForm):
    class Meta:
        model = Song
        fields = ["album_id"]
>>>>>>> 83fefc5155eb7fe7365e02a81fa9184b47738fc5
