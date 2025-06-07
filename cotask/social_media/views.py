from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def feed_view(request):
    return render(request, 'social_media/feed.html')


@login_required
def edit_profile(request):
    return render(request, 'social_media/edit_profile.html')


@login_required
def discover_view(request):
    return render(request, 'social_media/discover.html')


@login_required
def profile_view(request, username):
    return render(request, 'social_media/profile.html')
