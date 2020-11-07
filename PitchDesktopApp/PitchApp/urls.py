"""PitchDesktopApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    # path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/artist", ArtistSignUpView, name="artist_signup"),
    path(
        "accounts/signup/normal_user", NormalUserSignUpView, name="normal_user_signup"
    ),
    path("accounts/login", LoginView, name="login"),
    path("accounts/artist_home", ArtistHomeView, name="artist_home"),
    path("accounts/user_home", UserHomeView, name="user_home"),
    path("accounts/logout", LogoutView, name="logout"),
    path("album_upload", UploadAlbum, name="album_upload"),
    path("song_upload", UploadSong, name="song_upload"),
    path("podcast_upload", UploadPodcast, name="podcast_upload"),
    # path("form_check", FormCheck, name="form_check"),
    path("search_bar", SearchBarView, name="search_bar"),
    path("search_results", SearchResultView, name="search_results"),
    # path("form_check", FormCheck, name="form_check"),
    path("", HomeView, name="home"),
    # Testing
    path("queue", Queue, name="queue"),
    path("timesplayed", IncreaseTimesPLayed, name="timesPlayed"),
]
