import django.contrib.auth.decorators
import django.shortcuts
import django.http
import django.views.decorators.csrf
import django.contrib.auth.models

import social_media.models
import social_media.forms
import social_media.logic.following

import remember_line.logic.card_service


@django.contrib.auth.decorators.login_required
def feed_view(request: django.http.HttpRequest):
    return django.shortcuts.render(request, "social_media/feed.html")


@django.contrib.auth.decorators.login_required
@django.views.decorators.csrf.csrf_protect
def edit_profile(request: django.http.HttpRequest):
    try:
        profile = request.user.profile
    except social_media.models.Profile.DoesNotExist:
        profile = social_media.models.Profile.objects.create(user=request.user)

    if request.method == "POST":
        form = social_media.forms.UserProfileForm(
            request.POST, request.FILES, instance=profile
        )
        if form.is_valid():
            form.save()
            return django.shortcuts.redirect("profile", request.user.username)
    else:
        form = social_media.forms.UserProfileForm(instance=profile)
    return django.shortcuts.render(
        request,
        "social_media/edit_profile.html",
        {
            "form": form,
        },
    )


@django.contrib.auth.decorators.login_required
def discover_view(request: django.http.HttpRequest):
    return django.shortcuts.render(request, "social_media/discover.html")


@django.contrib.auth.decorators.login_required
def profile_view(request: django.http.HttpRequest, username):
    another_user = django.contrib.auth.models.User.objects.filter(
        username=username
    ).first()
    followers = social_media.logic.following.get_all_follower(another_user)
    followings = social_media.logic.following.get_all_following(another_user)
    lang_dictionaries = (
        remember_line.logic.card_service.get_lang_user_dictionaries(
            user=another_user,
        )
    )
    not_lang_dictionaries = (
        remember_line.logic.card_service.get_not_lang_user_dictionaries(
            user=another_user,
        )
    )
    return django.shortcuts.render(
        request,
        "social_media/profile.html",
        {
            "another_user": another_user,
            "is_following": social_media.logic.following.is_followed(
                request.user,
                another_user,
            ),
            "followers": followers,
            "followings": followings,
            "lang_dictionaries": lang_dictionaries,
            "not_lang_dictionaries": not_lang_dictionaries,
        },
    )


@django.contrib.auth.decorators.login_required
def follow_view(request: django.http.HttpRequest, username):
    another_user = django.contrib.auth.models.User.objects.filter(
        username=username
    ).first()
    social_media.logic.following.follow(request.user, another_user)
    return django.shortcuts.redirect("profile", username)


@django.contrib.auth.decorators.login_required
def unfollow_view(request: django.http.HttpRequest, username):
    another_user = django.contrib.auth.models.User.objects.filter(
        username=username
    ).first()
    social_media.logic.following.unfollow(request.user, another_user)
    return django.shortcuts.redirect("profile", username)


@django.contrib.auth.decorators.login_required
def followings_view(request, username=None):
    if username:
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.models.User, username=username
        )
    else:
        user = request.user

    followings = social_media.logic.following.get_all_following(user)

    return django.shortcuts.render(
        request,
        "social_media/followings.html",
        {
            "viewed_user": user,
            "followings": followings,
        },
    )


@django.contrib.auth.decorators.login_required
def followers_view(request, username=None):
    if username:
        user = django.shortcuts.get_object_or_404(
            django.contrib.auth.models.User, username=username
        )
    else:
        user = request.user

    followers = social_media.logic.following.get_all_follower(user)

    return django.shortcuts.render(
        request,
        "social_media/followers.html",
        {
            "viewed_user": user,
            "followers": followers,
        },
    )
