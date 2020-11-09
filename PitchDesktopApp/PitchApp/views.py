from django.http import request
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Features, Playlist, Podcast, User, Audio, Album, Artist, Song, Tag, AlbumBackUp
from .forms import (
    ArtistSignUpForm,
    NormalUserSignUpForm,
    AlbumUploadForm,
    SongUploadForm,
    PodcastUploadForm,
)
from django.http import JsonResponse
from django.contrib import messages
from django.core import serializers
import json
# Create your views here.


def ArtistSignUpView(request):
    if request.method == "POST":
        form = ArtistSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return redirect("/pitch/")
    else:
        form = ArtistSignUpForm()
    return render(request, "PitchApp/SignUpArtist.html", {"form": form})


def NormalUserSignUpView(request):
    if request.method == "POST":
        form = NormalUserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return redirect("/pitch/")
    else:
        form = NormalUserSignUpForm()
    return render(request, "PitchApp/SignUpUser.html", {"form": form})


def LoginView(request):
    if request.user.is_authenticated:
        if request.user.is_user:
            return redirect("/pitch/accounts/user_home")
        if request.user.is_artist:
            return redirect("/pitch/accounts/artist_home")
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            logged_in_user = User.objects.get(username=username)
            if logged_in_user.is_user:
                return redirect("/pitch/accounts/user_home")
            if logged_in_user.is_artist:
                return redirect("/pitch/accounts/artist_home")
        else:
            messages.error(request, "username or password not correct")
            return redirect("login")
    else:
        form = AuthenticationForm()
    return render(request, "PitchApp/Login.html", {"form": form})


def HomeView(request):
    print(request.user.username)
    return render(request, "PitchApp/home.html")


def ArtistHomeView(request):
    if request.user.is_artist:
        album_titles = Album.objects.filter(artist=request.user.id)
        stats = []
        for title in album_titles:
            album_times_played = 0
            songs = Song.objects.filter(
                album_id=title)
            for song in songs:
                audio = Audio.objects.get(title=song.audio_id)
                album_times_played += getattr(audio, "times_played")
            stats.append([title, album_times_played])
    return render(request, "PitchApp/ArtistHome.html", {"stats": stats})


@login_required(login_url="/pitch/accounts/login")
def AlbumStatsHomeView(request):
    if request.user.is_artist:
        album_titles = Album.objects.filter(artist=request.user.id)
        stats = []
        for title in album_titles:
            album_times_played = 0
            songs = Song.objects.filter(
                album_id=title)
            for song in songs:
                audio = Audio.objects.get(title=song.audio_id)
                album_times_played += getattr(audio, "times_played")
            stats.append([title, album_times_played])
        return render(request, "PitchApp/AlbumStatsHome.html", {"stats": stats})


def UserHomeView(request):
    trending_audio = Audio.objects.all().order_by('-times_played')[0:5]
    album_list = Album.objects.all()
    song_list = Song.objects.all()
    all_albums = []
    for audio in trending_audio:
        for song in song_list:
            if str(audio.title) == str(song.audio_id):
                for album in album_list:
                    if str(album.title) == str(song.album_id):
                        all_albums.append(
                            Album.objects.get(title=song.album_id))
    for album in all_albums:
        print(album.cover_file)
    objects_list = list(zip(trending_audio, all_albums))
    return render(request, "PitchApp/UserHome.html", {"objects_list": objects_list})


def LogoutView(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/pitch/accounts/login")
def UploadAlbum(request):
    if request.user.is_artist:
        if request.method == "POST":
            form = AlbumUploadForm(request.POST, request.FILES)
            if form.is_valid():
                album = form.save(commit=False)
                artist_obj = Artist.objects.get(user=request.user.id)
                album.artist = artist_obj
                album.save()
                return redirect('artist_home')
        else:
            form = AlbumUploadForm()
        return render(request, "PitchApp/UploadAlbum.html", {"form": form})


@login_required(login_url="/pitch/accounts/login")
def UploadSong(request):
    if request.user.is_artist:
        if request.method == "POST":
            form = SongUploadForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data["title"]
                duration = form.cleaned_data["duration"]
                audio_file = form.cleaned_data["audio_file"]
                tags = form.cleaned_data["tags"]
                album_name = form.cleaned_data["album_name"]
                audio = Audio(
                    title=title,
                    duration=duration,
                    times_played=0,
                    audio_file=audio_file,
                )
                audio.save()
                artist_deatils = Artist.objects.get(user=request.user.id)
                album = Album.objects.get(
                    artist=artist_deatils, title=album_name)
                new_song = Song.objects.create(audio_id=audio, album_id=album)
                artist_deatils.save()
                new_song.save()
                tag1, tag2, tag3 = tags.split(",")
                song_tag = Tag(audio_id=audio, tag1=tag1, tag2=tag2, tag3=tag3)
                song_tag.save()
                return redirect('artist_home')

        else:
            form = SongUploadForm()
        return render(request, "PitchApp/UploadSong.html", {"form": form})
    else:
        return render(request, "ErrorPage.html")


@login_required(login_url="/pitch/accounts/login")
def UploadPodcast(request):
    if request.user.is_artist:
        if request.method == "POST":
            form = PodcastUploadForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data["title"]
                duration = form.cleaned_data["duration"]
                audio_file = form.cleaned_data["audio_file"]
                tags = form.cleaned_data["tags"]
                album_name = form.cleaned_data["album_name"]
                audio = Audio(
                    title=title,
                    duration=duration,
                    times_played=0,
                    audio_file=audio_file,
                )
                audio.save()
                artist_deatils = Artist.objects.get(user=request.user.id)
                album = Album.objects.get(
                    artist=artist_deatils, title=album_name)
                new_podcast = Podcast(audio_id=audio, album_id=album)
                artist_deatils.save()
                new_podcast.save()
                tag1, tag2, tag3 = tags.split(",")
                song_tag = Tag(audio_id=audio, tag1=tag1, tag2=tag2, tag3=tag3)
                song_tag.save()
                return redirect('artist_home')
        else:
            form = PodcastUploadForm()
        return render(request, "PitchApp/UploadPodcast.html", {"form": form})
    else:
        return render(request, "ErrorPage.html")
# def FormCheck(request):
#     form = SongUploadForm()
#     return render(request, "FormCheck.html", {"form": form})


def SearchBarView(request):
    return render(request, "PitchApp/SearchBar.html")


def SearchResult(request):
    item_type = request.GET["item_type"]
    print(item_type)
    query = request.GET["search_bar"]
    query_list = Audio.objects.filter(title__icontains=query).values_list(
        "title", flat=True
    )
    all_songs = Song.objects.all()
    all_podcasts = Podcast.objects.all()
    all_albums = []
    all_results = []
    if item_type == "Song":
        for each_song in all_songs:
            if str(each_song.audio_id) in query_list:
                all_results.append(Audio.objects.get(title=each_song.audio_id))
                all_albums.append(Album.objects.get(title=each_song.album_id))
    if item_type == "Podcast":
        for each_podcast in all_podcasts:
            if str(each_podcast.audio_id) in query_list:
                all_results.append(Audio.objects.get(
                    title=each_podcast.audio_id))
    print(all_results)
    objects_list = list(zip(all_results, all_albums))
    return render(request, "PitchApp/SearchReults.html", {"objects_list": objects_list})


@login_required(login_url="/pitch/accounts/login")
def AlbumUpdateView(request, album_id):
    if request.user.is_artist:
        album_obj = Album.objects.get(title=album_id, artist=request.user.id)
        form = AlbumUploadForm(
            request.POST or None, request.FILES or None, instance=album_obj
        )
        if form.is_valid() and album_obj is not None:
            backup_album = AlbumBackUp(
                title=album_obj.title,
                year=album_obj.year,
                cover_file=album_obj.cover_file,
                artist=album_obj.artist,
            )
            backup_album.save()
            form.save()
        return render(request, "PitchApp/UpdateAlbum.html", {"form": form})


def Queue(request):
    audio_files = Audio.objects.all()
    return render(request, "Drafts/audioQueue.html", {"audio_files": audio_files})


def IncreaseTimesPLayed(request):
    title_dict = request.GET
    title = title_dict["title"]
    audio_file = Audio.objects.get(title=title)
    times_played = audio_file.times_played
    audio_file.times_played = times_played + 1
    audio_file.save()
    return JsonResponse({"timesPlayed": audio_file.times_played})


@login_required(login_url="/pitch/accounts/login")
def AddToPlaylistView(request):
    title_dict = request.GET
    title = title_dict["title"]
    if request.user.is_user:
        favourites_playlist = Playlist.objects.get(title="Favourites")
        audio_file = Audio.objects.get(title=title)
        feature_obj = Features.objects.create(
            audio_id=audio_file, playlist_id=favourites_playlist
        )
        feature_obj.save()
        print("hello")
    return JsonResponse({"Hello": "successfull"})


@login_required(login_url="/pitch/accounts/login")
def AlbumStats(request, album_id):
    if request.user.is_artist:
        album = Album.objects.get(title=album_id, artist=request.user.id)
        album_title = getattr(album, "title")
        songs = Song.objects.filter(album_id=album)
        stats = []
        for song in songs:
            audio_id = getattr(song, "audio_id")
            audio = Audio.objects.get(title=audio_id)
            times_played = getattr(audio_id, "times_played")
            stats.append([audio_id, times_played])
        return render(request, "PitchApp/AlbumStats.html", {"stats": stats, "album": album})


def Trending(request):
    audios = Audio.objects.all().order_by('-times_played')
    return render(request, "PitchApp/Trending.html", {'audios': audios})


def PaymentView(request):
    return render(request, "PitchApp/payment.html")
