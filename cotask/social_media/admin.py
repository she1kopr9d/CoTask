import django.contrib.admin

import social_media.models


django.contrib.admin.site.register(social_media.models.FollowRelation)
django.contrib.admin.site.register(social_media.models.Profile)
