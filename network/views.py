from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User,Post, Like

class NewPostForm(forms.Form):
    newPost = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Say something', 'class': 'form-control form-group col-6'})
    )


def index(request):
    create_post(request)

    posts = Post.objects.all().order_by("-created_at")

    for post in posts:
        post.is_liked = False
        if request.user.is_authenticated:
            post.is_liked = post.is_liked_by_user(request.user)

    return render(request, "network/index.html", {
        "newPostForm": NewPostForm(),
        "posts": posts
    })

def create_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = Post(
                user=request.user, 
                content=form.cleaned_data["newPost"])
            post.save()
            # Redirect to the index page to update the list of entries
            return HttpResponseRedirect(reverse('index'))

def like_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        try:
            # Try to fetch the existing 'Like' object.
            like = Like.objects.get(user=request.user, post=post)
            # Since the object exists, we assume the user wants to unlike the post.
            like.delete()
            is_liked = False
        except ObjectDoesNotExist:
            # If the 'Like' object doesn't exist, create a new one indicating a like action.
            Like.objects.create(user=request.user, post=post)
            is_liked = True
        
        # After handling the like/unlike logic, return the current like count and status.
        return JsonResponse({'like_count': post.like_count, 'liked': is_liked})



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
