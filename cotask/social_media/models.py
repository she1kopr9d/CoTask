from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="user",
        related_name="profile"
    )

    avatar = models.ImageField(
        verbose_name="avatar",
        upload_to='avatars/',
        blank=True,
        null=True
    )

    # Добавляем недостающее поле
    about = models.TextField(
        verbose_name="О себе",
        blank=True,
        null=True,
        default=""
    )

    following = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True,
        verbose_name='подписки',
        through='FollowRelation'
    )

    def save(self, *args, **kwargs):
        # Сжатие только при создании/изменении изображения
        if self.avatar and (not self.pk or Profile.objects.get(pk=self.pk).avatar != self.avatar):
            img = Image.open(self.avatar)

            # Конвертировать в RGB (для формата JPEG)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Создать thumbnail (сохранение пропорций)
            img.thumbnail((200, 200))

            # Сохранить в памяти
            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            # Переопределить оригинальный файл
            self.avatar = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{self.avatar.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        super().save(*args, **kwargs)


class FollowRelation(models.Model):
    follower = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follow_relations_as_follower'
    )
    following = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='follow_relations_as_following'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('follower', 'following')]  # Запрет дублирования подписок
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'
