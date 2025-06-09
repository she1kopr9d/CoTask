import social_media.models


def follow(user, another_user):
    rel = social_media.models.FollowRelation(
        follower=user.profile,
        following=another_user.profile,
    )
    rel.save()


def unfollow(user, another_user):
    rel = social_media.models.FollowRelation.objects.filter(
        follower=user.profile,
        following=another_user.profile,
    ).first()
    rel.delete()


def is_followed(user, another_user) -> bool:
    return social_media.models.FollowRelation.objects.filter(
        follower=user.profile,
        following=another_user.profile,
    ).count() != 0


def get_all_follower(user) -> list:
    rels = social_media.models.FollowRelation.objects.filter(
        following=user.profile
    ).all()
    return [
        rel.follower.user
        for rel in rels
    ]


def get_all_following(user) -> list:
    rels = social_media.models.FollowRelation.objects.filter(
        follower=user.profile
    ).all()
    return [
        rel.following.user
        for rel in rels
    ]
