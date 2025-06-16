import django.contrib.auth

import remember_line.models


User = django.contrib.auth.get_user_model()


def create_or_update_association(
    card: remember_line.models.Card,
    user: User,
    text=None,
    image=None,
    phrase=None,
):
    assoc, _ = remember_line.models.CardAssociation.objects.get_or_create(
        card=card,
        user=user,
    )
    if text is not None:
        assoc.text = text
    if image is not None:
        assoc.image = image
    if phrase is not None:
        assoc.example_phrase = phrase
    assoc.save()
    return assoc


def get_user_association(card: remember_line.models.Card, user: User):
    return remember_line.models.CardAssociation.objects.filter(
        card=card,
        user=user,
    ).first()
