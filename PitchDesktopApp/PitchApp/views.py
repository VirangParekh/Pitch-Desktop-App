from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
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
        print("Enter POST")
        form = AuthenticationForm(request.POST)
        print("Form Initialized")
        # print("Valid Form")
        username = request.POST["username"]
        print(username)
        password = request.POST["password"]
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


def LogoutView(request):
    logout(request)
    return render(request, "PitchApp/Logout.html")
