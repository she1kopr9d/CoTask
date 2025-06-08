from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Profile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="user"
    )

    avatar = models.ImageField(upload_to='avatars/')

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
