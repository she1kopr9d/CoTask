from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Dictionary(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_dictionaries')
    shared_with = models.ManyToManyField(User, related_name='shared_dictionaries', blank=True)

    is_language = models.BooleanField(default=False, verbose_name="Языковой словарь")
    is_public = models.BooleanField(default=False, verbose_name="Публичный доступ")

    def __str__(self):
        return self.name


class Card(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='cards')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    front = models.CharField(max_length=255)  # Слово/выражение
    back = models.TextField()  # Перевод/объяснение

    def __str__(self):
        return self.front


class CardAssociation(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='associations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='associations')
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='association_images/', blank=True, null=True)
    example_phrase = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('card', 'user')

    def __str__(self):
        return f'Ассоциация {self.user.username} к "{self.card.front}"'


class CardReview(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    last_reviewed = models.DateTimeField(auto_now=True)
    next_review = models.DateTimeField(default=timezone.now)
    ease_factor = models.FloatField(default=2.5)
    interval = models.IntegerField(default=1)
    repetitions = models.IntegerField(default=0)

    def schedule_next_review(self, quality):
        """
        SM-2 алгоритм: качество от 0 до 5
        """
        if quality < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)

            self.repetitions += 1
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        self.next_review = timezone.now() + timedelta(days=self.interval)
        self.save()
