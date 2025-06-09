import social_media.models


def create_profile(user) -> social_media.models.Profile:
    profile = social_media.models.Profile(
        user=user,
        avatar="avatars/default_avatar.png",
        about="",
    )
    profile.save()
    return profile
