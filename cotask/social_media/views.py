from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User
from social_media.models import Profile
from social_media.forms import UserProfileForm


import social_media.logic.following



@login_required
def feed_view(request: HttpRequest):
    return render(request, 'social_media/feed.html')


@login_required
@csrf_protect
def edit_profile(request: HttpRequest):
    try:
        profile = request.user.profile  # Получаем профиль текущего пользователя
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)  # Создаем, если нет

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)  # Редирект после успеха
    else:
        form = UserProfileForm(instance=profile)
    return render(
        request,
        'social_media/edit_profile.html',
        {
            "form": form,
        },
    )


@login_required
def discover_view(request: HttpRequest):
    return render(request, 'social_media/discover.html')


@login_required
def profile_view(request: HttpRequest, username):
    another_user = User.objects.filter(username=username).first()
    followers = social_media.logic.following.get_all_follower(another_user)
    followings = social_media.logic.following.get_all_following(another_user)
    return render(
        request,
        'social_media/profile.html',
        {
            "another_user": another_user,
            "is_following": social_media.logic.following.is_followed(
                request.user,
                another_user,
            ),
            "followers": followers,
            "followings": followings,
        },
    )


@login_required
def follow_view(request: HttpRequest, username):
    another_user = User.objects.filter(username=username).first()
    social_media.logic.following.follow(request.user, another_user)
    return redirect("profile", username)


@login_required
def unfollow_view(request: HttpRequest, username):
    another_user = User.objects.filter(username=username).first()
    social_media.logic.following.unfollow(request.user, another_user)
    return redirect("profile", username)
