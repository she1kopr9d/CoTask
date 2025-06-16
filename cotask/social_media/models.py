import PIL.Image

import django.contrib.auth.models
import django.db.models


class Profile(django.db.models.Model):

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        verbose_name="user",
        related_name="profile",
    )

    avatar = django.db.models.ImageField(
        verbose_name="avatar", upload_to="avatars/", blank=True, null=True
    )

    about = django.db.models.TextField(
        verbose_name="О себе", blank=True, null=True, default=""
    )

    following = django.db.models.ManyToManyField(
        "self",
        related_name="followers",
        symmetrical=False,
        blank=True,
        verbose_name="подписки",
        through="FollowRelation",
    )

    def save(self, *args, **kwargs):
        super().save()
        img = PIL.Image.open(self.avatar.path)
        if img.height > img.width:
            left = 0
            right = img.width
            top = (img.height - img.width) / 2
            bottom = (img.height + img.width) / 2
            img = img.crop((left, top, right, bottom))
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
        elif img.width > img.height:
            left = (img.width - img.height) / 2
            right = (img.width + img.height) / 2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


class FollowRelation(django.db.models.Model):
    follower = django.db.models.ForeignKey(
        Profile,
        on_delete=django.db.models.CASCADE,
        related_name="follow_relations_as_follower",
    )
    following = django.db.models.ForeignKey(
        Profile,
        on_delete=django.db.models.CASCADE,
        related_name="follow_relations_as_following",
    )
    created_at = django.db.models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("follower", "following")]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.follower} подписан на {self.following}"
