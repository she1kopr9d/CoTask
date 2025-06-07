from django.urls import path

import social_media.views


urlpatterns = [
    path('feed/', social_media.views.feed_view, name='feed'),
    path('profile/<str:username>/', social_media.views.profile_view, name='profile'),
    path('discover/', social_media.views.discover_view, name='discover'),
    path('edit-profile/', social_media.views.edit_profile, name='edit_profile'),
]
