from remember_line.models import Card, Dictionary
from django.contrib.auth import get_user_model

User = get_user_model()


def create_dictionary(
    name: str,
    creator: User,
    is_language: bool,
    is_public: bool,
) -> Dictionary:
    return Dictionary.objects.create(
        name=name,
        creator=creator,
        is_language=is_language,
        is_public=is_public,
    )


def share_dictionary(dictionary: Dictionary, user: User):
    dictionary.shared_with.add(user)


def create_card(dictionary: Dictionary, creator: User, front: str, back: str) -> Card:
    return Card.objects.create(
        dictionary=dictionary,
        creator=creator,
        front=front,
        back=back
    )


def get_user_dictionaries(creator: User):
    return Dictionary.objects.filter(
        is_public=True,
        creator=creator,
    ).all()


def get_lang_user_dictionaries(creator: User):
    return Dictionary.objects.filter(
        is_public=True,
        creator=creator,
        is_language=True,
    ).all()


def get_not_lang_user_dictionaries(creator: User):
    return Dictionary.objects.filter(
        is_public=True,
        creator=creator,
        is_language=False,
    ).all()
