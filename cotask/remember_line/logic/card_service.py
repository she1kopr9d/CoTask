from remember_line.models import Card, Dictionary, CardReview
from django.contrib.auth import get_user_model
from django.db.models import Q

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


def create_card_review(
    card: Card,
    user: User,
):
    return CardReview.objects.create(
        card=card,
        user=user,
    )


def get_user_dictionaries(user: User):
    return Dictionary.objects.filter(
        is_public=True
    ).filter(
        Q(creator=user) | Q(shared_with=user)
    ).distinct()


def get_lang_user_dictionaries(user: User):
    return Dictionary.objects.filter(
        is_public=True,
        is_language=True
    ).filter(
        Q(creator=user) | Q(shared_with=user)
    ).distinct()


def get_not_lang_user_dictionaries(user: User):
    return Dictionary.objects.filter(
        is_public=True,
        is_language=False
    ).filter(
        Q(creator=user) | Q(shared_with=user)
    ).distinct()
