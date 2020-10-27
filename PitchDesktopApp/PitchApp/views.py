from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import User
from .forms import ArtistSignUpForm, NormalUserSignUpForm

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
            # login(request=request, user=user)
            return redirect("/pitch/")
    else:
        form = NormalUserSignUpForm()
    return render(request, "PitchApp/SignUpUser.html", {"form": form})


def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request=request, username=username, password=password)
            print(user)
            login(request=request, user=user)
            print("Login successful")
            logged_in_user = User.objects.get(username=username)
            if logged_in_user.is_user:
                return redirect("/pitch/accounts/user_home")
            if logged_in_user.is_artist:
                return redirect("/pitch/accounts/artist_home")
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
