from django.contrib import admin
from social_media.models import Profile, FollowRelation

# Register your models here.
admin.site.register(FollowRelation)
admin.site.register(Profile)
