import django.urls

import social_media.views


urlpatterns = [
    django.urls.path("feed/", social_media.views.feed_view, name="feed"),
    django.urls.path(
        "profile/<str:username>/",
        social_media.views.profile_view,
        name="profile",
    ),
    django.urls.path(
        "discover/", social_media.views.discover_view, name="discover"
    ),
    django.urls.path(
        "edit-profile/", social_media.views.edit_profile, name="edit_profile"
    ),
    django.urls.path(
        "follow/<str:username>/", social_media.views.follow_view, name="follow"
    ),
    django.urls.path(
        "unfollow/<str:username>/",
        social_media.views.unfollow_view,
        name="unfollow",
    ),
    django.urls.path(
        "followings/", social_media.views.followings_view, name="my_followings"
    ),
    django.urls.path(
        "users/<str:username>/followings/",
        social_media.views.followings_view,
        name="user_followings",
    ),
    django.urls.path(
        "followers/", social_media.views.followers_view, name="my_followers"
    ),
    django.urls.path(
        "users/<str:username>/followers/",
        social_media.views.followers_view,
        name="user_followers",
    ),
]
