from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest


@login_required
def feed_view(request: HttpRequest):
    return render(request, 'social_media/feed.html')


@login_required
def edit_profile(request: HttpRequest):
    return render(request, 'social_media/edit_profile.html')


@login_required
def discover_view(request: HttpRequest):
    return render(request, 'social_media/discover.html')


@login_required
def profile_view(request: HttpRequest, username):
    if request.user.username == username:
        return render(request, 'social_media/self_profile.html')
    return render(request, 'social_media/profile.html')
