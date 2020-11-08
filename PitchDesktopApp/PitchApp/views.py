from datetime import datetime, date
from django.http import request
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import (
    AlbumBackUp,
    Features,
    NormalUser,
    Playlist,
    Podcast,
    User,
    Audio,
    Album,
    Artist,
    Song,
    Tag,
    Subscription,
)
from .forms import (
    ArtistSignUpForm,
    NormalUserSignUpForm,
    AlbumUploadForm,
    SongUploadForm,
    PodcastUploadForm,
    SubscriptionForm,
)
from django.http import JsonResponse
from django.contrib import messages

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
        user = authenticate(request=request, username=username, password=password)
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
    return render(request, "PitchApp/ArtistHome.html")


def UserHomeView(request):
    return render(request, "PitchApp/UserHome.html")


def LogoutView(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/pitch/accounts/login")
def UploadAlbum(request):
    if request.user.is_artist:
        if request.method == "POST":
            form = AlbumUploadForm(request.POST)
            if form.is_valid():
                album = form.save(commit=False)
                album.artist = request.user.id
                album.save()
        else:
            form = AlbumUploadForm()
        return render(request, "PitchApp/UploadAlbum.html", {"form": form})


@login_required(login_url="/pitch/accounts/login")
def UploadSong(request):
    if request.user.is_artist:
        if request.method == "POST":
            form = SongUploadForm(request.POST)
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
                artist_deatils = Artist.objects.filter(user=request.user.id)
                album = Album.objects.get_or_create(
                    artist=artist_deatils.id, title=album_name
                )
                new_song = Song(audio_id=audio.id, album_id=album.id)
                audio.save()
                artist_deatils.save()
                new_song.save()
                tag1, tag2, tag3 = tags.split(",")
                song_tag = Tag(audio_id=audio.id, tag1=tag1, tag2=tag2, tag3=tag3)
                song_tag.save()

        else:
            form = SongUploadForm()
        return render(request, "PitchApp/UploadSong.html", {"form": form})
    else:
        return render(request, "ErrorPage.html")


@login_required(login_url="/pitch/accounts/login")
def UploadPodcast(request):
    if request.user.is_artist:
        if request.method == "POST":
            form = SongUploadForm(request.POST)
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
                artist_deatils = Artist.objects.filter(user=request.user.id)
                album = Album.objects.get_or_create(
                    artist=artist_deatils.id, title=album_name
                )
                new_podcast = Podcast(audio_id=audio.id)
                audio.save()
                artist_deatils.save()
                new_podcast.save()
                tag1, tag2, tag3 = tags.split(",")
                song_tag = Tag(audio_id=audio.id, tag1=tag1, tag2=tag2, tag3=tag3)
                song_tag.save()

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


def SearchResultView(request):
    item_type = request.GET["item_type"]
    print(item_type)
    query = request.GET["search_bar"]
    query_list = Audio.objects.filter(title__icontains=query).values_list(
        "title", flat=True
    )
    all_songs = Song.objects.all()
    all_podcasts = Podcast.objects.all()
    all_results = []
    if item_type == "Song":
        for each_song in all_songs:
            if str(each_song.audio_id) in query_list:
                all_results.append(Audio.objects.get(title=each_song.audio_id))
    if item_type == "Podcast":
        for each_podcast in all_podcasts:
            if str(each_podcast.audio_id) in query_list:
                all_results.append(Audio.objects.get(title=each_podcast.audio_id))
    return render(request, "PitchApp/SearchReults.html", {"all_results": all_results})


@login_required(login_url="/pitch/accounts/login")
def AlbumUpdateView(request, album_id):
    if request.user.is_artist:
        album_obj = Album.objects.get(id=album_id, artist=request.user.id)
        form = AlbumUploadForm(request.POST or None, instance=album_obj)
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
def AddToPlaylistView(request, audio_id):
    if request.user.is_user:
        favourites_playlist = Playlist.objects.get(title="Favourites")
        feature_obj = Features.objects.create(
            audio_id=audio_id, playlist_id=favourites_playlist.id
        )
        feature_obj.save()


@login_required(login_url="/pitch/accounts/login")
def AlbumStats(request, album_id):
    if request.user.is_artist:
        album = Album.objects.get(id=album_id, artist=request.user.id)
        album_title = getattr(album, "title")
        songs = Song.objects.filter(album_id=album_title)
        stats = []
        for song in songs:
            audio_id = getattr(song, "audio_id")
            audio = Audio.objects.get(title=audio_id)
            times_played = getattr(audio_id, "times_played")
            stats.append([audio_id, times_played])
        return render(request, "PitchApp/AlbumStats.html", {"stats": stats})


def Trending(request):
    audios = Audio.objects.all().order_by("-times_played")
    return render(request, "PitchApp/Trending.html", {"audios": audios})


def SubscriptionView(request):
    if request.user.is_user:
        context = {}
        if request.method == "POST":
            form = SubscriptionForm(request.POST)
            context["form"] = form
            if form.is_valid():
                user_get = NormalUser(user=request.user.id)
                user_get.card = form.cleaned_data["card"]
                due_date = form.cleaned_data["due_date"]
                subscription = Subscription(user_id=request.user.id, due_date=due_date)
                checkout_price = ((due_date - date.today()).days) * 3.33
                context["price"] = checkout_price
                user_get.save()
                subscription.save()
                return redirect("/")
        else:
            form = SubscriptionForm()
            context["form"] = form
        return render(request, "PitchApp/Subscription.html", context)
