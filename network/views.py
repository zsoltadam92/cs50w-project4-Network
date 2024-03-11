from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


from .models import User,Post, Like, Follow

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

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    # Check if current user is following the profile
    is_following = False
    if request.user.is_authenticated and Follow.objects.filter(follower=request.user, followed=user).exists():
        is_following = True

    # Count the number of followers and following
    followers_count = Follow.objects.filter(followed=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    return render(request, 'network/profile.html', {
        'user_profile': user,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count
    })

@login_required
def toggle_follow(request, username):
    if request.method == 'POST':
        follower = request.user
        followed = User.objects.get(username=username)

        if follower == followed:
            return JsonResponse({"error": "You cannot follow yourself."}, status=400)

        try:
            # Try to find an existing follow relationship
            follow_relation = Follow.objects.get(follower=follower, followed=followed)
            # If found, delete it, meaning the user wants to unfollow
            follow_relation.delete()
            action = "unfollowed"
        except Follow.DoesNotExist:
            # If not found, create a new follow relationship, meaning the user wants to follow
            Follow.objects.create(follower=follower, followed=followed)
            action = "followed"

        return JsonResponse({"status": "success", "action": action, "followers_count": Follow.objects.filter(followed=followed).count()})

    return JsonResponse({"error": "POST request required."}, status=400)

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
