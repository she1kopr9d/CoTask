from django.urls import path

import social_media.views


urlpatterns = [
    path('feed/', social_media.views.feed_view, name='feed'),
    path('profile/<str:username>/', social_media.views.profile_view, name='profile'),
    path('discover/', social_media.views.discover_view, name='discover'),
    path('edit-profile/', social_media.views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', social_media.views.follow_view, name='follow'),
    path('unfollow/<str:username>/', social_media.views.unfollow_view, name='unfollow'),
    path('followings/', social_media.views.followings_view, name='my_followings'),
    path('users/<str:username>/followings/', social_media.views.followings_view, name='user_followings'),
    path('followers/', social_media.views.followers_view, name='my_followers'),
    path('users/<str:username>/followers/', social_media.views.followers_view, name='user_followers')
]
