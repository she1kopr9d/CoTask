import datetime

import django.utils

import remember_line.models


def get_or_create_review(card, user):
    obj, _ = remember_line.models.CardReview.objects.get_or_create(
        card=card,
        user=user,
    )
    return obj


def add_all_review(user, dictionary):
    cards = remember_line.models.Card.objects.filter(
        dictionary=dictionary
    ).all()

    for card in cards:
        get_or_create_review(card, user)


def schedule_review(review: remember_line.models.CardReview, quality: int):
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
            review.ease_factor
            + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)),
        )

    review.next_review = django.utils.timezone.now() + datetime.timedelta(
        days=review.interval,
    )
    review.save()
    return review
