import json
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        following_users = list(following_users) + [request.user.id]
        posts = Post.objects.filter(user__id__in=following_users).order_by('-timestamp')
    else:
        posts = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_posts = []

    if request.user.is_authenticated:
        liked_posts = [like.post.id for like in Like.objects.filter(user=request.user)]

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })


def explore(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_posts = []

    if request.user.is_authenticated:
        liked_posts = [like.post.id for like in Like.objects.filter(user=request.user)]

    return render(request, "network/explore.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        if content:
            post = Post(user=request.user, content=content)
            post.save()

        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))


def profile(request, user_id):
    try:
        user_profile = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    posts = Post.objects.filter(user=user_profile).order_by('-timestamp')
    followers = Follow.objects.filter(following=user_profile).count()
    following = Follow.objects.filter(follower=user_profile).count()
    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_posts = []

    if request.user.is_authenticated:
        liked_posts = [like.post.id for like in Like.objects.filter(user=request.user)]

    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "page_obj": page_obj,
        "followers": followers,
        "following": following,
        "is_following": is_following,
        "liked_posts": liked_posts
    })


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "network/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        data = request.POST.copy()  # Make mutable copy
        if 'password' in data:
            data['password1'] = data['password']
        if 'confirmation' in data:
            data['password2'] = data['confirmation']

        form = CustomUserCreationForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "network/register.html", {
        "form": form
    })


@login_required
def follow(request, user_id):
    try:
        user_to_follow = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    if user_to_follow == request.user:
        return HttpResponseRedirect(reverse("profile", args=(user_id,)))

    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

    return HttpResponseRedirect(reverse("profile", args=(user_id,)))


@login_required
def unfollow(request, user_id):
    try:
        user_to_unfollow = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))

    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()

    return HttpResponseRedirect(reverse("profile", args=(user_id,)))


@login_required
def following(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    liked_posts = [like.post.id for like in Like.objects.filter(user=request.user)]

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })


@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if post.user != request.user:
        return JsonResponse({"error": "Not authorized"}, status=403)

    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data.get("content", "")
        post.save()
        return JsonResponse({"message": "Post updated successfully"}, status=200)

    return JsonResponse({"error": "PUT request required"}, status=400)


@csrf_exempt
@login_required
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    like_exists = Like.objects.filter(user=request.user, post=post).exists()

    if like_exists:
        Like.objects.filter(user=request.user, post=post).delete()
        liked = False
    else:
        like = Like(user=request.user, post=post)
        like.save()
        liked = True

    like_count = Like.objects.filter(post=post).count()

    return JsonResponse({
        "liked": liked,
        "like_count": like_count
    })
