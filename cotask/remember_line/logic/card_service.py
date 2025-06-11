from remember_line.models import Card, Dictionary
from django.contrib.auth import get_user_model

User = get_user_model()


def create_dictionary(name: str, creator: User) -> Dictionary:
    return Dictionary.objects.create(name=name, creator=creator)


def share_dictionary(dictionary: Dictionary, user: User):
    dictionary.shared_with.add(user)


def create_card(dictionary: Dictionary, creator: User, front: str, back: str) -> Card:
    return Card.objects.create(
        dictionary=dictionary,
        creator=creator,
        front=front,
        back=back
    )
