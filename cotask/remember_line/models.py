import datetime

import django.contrib.auth
import django.db.models
import django.utils.timezone


User = django.contrib.auth.get_user_model()


class Dictionary(django.db.models.Model):
    name = django.db.models.CharField(max_length=255)
    creator = django.db.models.ForeignKey(
        User,
        on_delete=django.db.models.CASCADE,
        related_name="created_dictionaries",
    )
    shared_with = django.db.models.ManyToManyField(
        User, related_name="shared_dictionaries", blank=True
    )

    is_language = django.db.models.BooleanField(
        default=False, verbose_name="Языковой словарь"
    )
    is_public = django.db.models.BooleanField(
        default=False, verbose_name="Публичный доступ"
    )

    def __str__(self):
        return self.name


class Card(django.db.models.Model):
    dictionary = django.db.models.ForeignKey(
        Dictionary, on_delete=django.db.models.CASCADE, related_name="cards"
    )
    creator = django.db.models.ForeignKey(
        User, on_delete=django.db.models.CASCADE, related_name="cards"
    )
    front = django.db.models.CharField(max_length=255)  # Слово/выражение
    back = django.db.models.TextField()  # Перевод/объяснение

    def __str__(self):
        return self.front


class CardAssociation(django.db.models.Model):
    card = django.db.models.ForeignKey(
        Card, on_delete=django.db.models.CASCADE, related_name="associations"
    )
    user = django.db.models.ForeignKey(
        User, on_delete=django.db.models.CASCADE, related_name="associations"
    )
    text = django.db.models.TextField(blank=True, null=True)
    image = django.db.models.ImageField(
        upload_to="association_images/", blank=True, null=True
    )
    example_phrase = django.db.models.TextField(blank=True, null=True)
    created_at = django.db.models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ассоциация {self.user.username} к "{self.card.front}"'


class CardReview(django.db.models.Model):
    card = django.db.models.ForeignKey(
        Card, on_delete=django.db.models.CASCADE, related_name="reviews"
    )
    user = django.db.models.ForeignKey(
        User, on_delete=django.db.models.CASCADE, related_name="reviews"
    )
    last_reviewed = django.db.models.DateTimeField(auto_now=True)
    next_review = django.db.models.DateTimeField(
        default=django.utils.timezone.now
    )
    ease_factor = django.db.models.FloatField(default=2.5)
    interval = django.db.models.IntegerField(default=1)
    repetitions = django.db.models.IntegerField(default=0)

    def schedule_next_review(self, quality):
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
            self.ease_factor = max(
                1.3,
                self.ease_factor
                + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)),
            )

        self.next_review = django.utils.timezone.now() + datetime.timedelta(
            days=self.interval
        )
        self.save()
