from remember_line.models import Card, CardAssociation
from django.contrib.auth import get_user_model

User = get_user_model()


def create_or_update_association(card: Card, user: User, text=None, image=None, phrase=None):
    assoc, _ = CardAssociation.objects.get_or_create(card=card, user=user)
    if text is not None:
        assoc.text = text
    if image is not None:
        assoc.image = image
    if phrase is not None:
        assoc.example_phrase = phrase
    assoc.save()
    return assoc


def get_user_association(card: Card, user: User):
    return CardAssociation.objects.filter(card=card, user=user).first()
