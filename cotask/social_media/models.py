import sys
import io
import PIL.Image

import django.db.models
import django.contrib.auth.models
import django.core.files.uploadedfile


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
        if self.avatar and (
            not self.pk
            or Profile.objects.get(pk=self.pk).avatar != self.avatar
        ):
            img = PIL.Image.open(self.avatar)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((200, 200))

            output = io.BytesIO()
            img.save(output, format="JPEG", quality=90)
            output.seek(0)

            self.avatar = django.core.files.uploadedfile.InMemoryUploadedFile(
                output,
                "ImageField",
                f"{self.avatar.name.split('.')[0]}.jpg",
                "image/jpeg",
                sys.getsizeof(output),
                None,
            )
        super().save(*args, **kwargs)


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
