from remember_line.models import CardReview
from django.utils import timezone
from datetime import timedelta


def get_or_create_review(card, user):
    obj, _ = CardReview.objects.get_or_create(card=card, user=user)
    return obj


def schedule_review(review: CardReview, quality: int):
    """
    Обновляет карточку повторения по алгоритму SM-2.
    quality: 0-5
    """
    if quality < 3:
        review.repetitions = 0
        review.interval = 1
    else:
        if review.repetitions == 0:
            review.interval = 1
        elif review.repetitions == 1:
            review.interval = 6
        else:
            review.interval = int(review.interval * review.ease_factor)

        review.repetitions += 1
        review.ease_factor = max(
            1.3,
            review.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )

    review.next_review = timezone.now() + timedelta(days=review.interval)
    review.save()
    return review
