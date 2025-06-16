import django.contrib.auth
import django.db.models

import remember_line.models


User = django.contrib.auth.get_user_model()


def create_dictionary(
    name: str,
    creator: User,
    is_language: bool,
    is_public: bool,
) -> remember_line.models.Dictionary:
    return remember_line.models.Dictionary.objects.create(
        name=name,
        creator=creator,
        is_language=is_language,
        is_public=is_public,
    )


def share_dictionary(dictionary: remember_line.models.Dictionary, user: User):
    dictionary.shared_with.add(user)


def create_card(
    dictionary: remember_line.models.Dictionary,
    creator: User,
    front: str,
    back: str,
) -> remember_line.models.Card:
    return remember_line.models.Card.objects.create(
        dictionary=dictionary, creator=creator, front=front, back=back
    )


def create_card_review(
    card: remember_line.models.Card,
    user: User,
):
    return remember_line.models.CardReview.objects.create(
        card=card,
        user=user,
    )


def get_user_dictionaries(user: User):
    return (
        remember_line.models.Dictionary.objects.filter(is_public=True)
        .filter(
            django.db.models.Q(creator=user)
            | django.db.models.Q(shared_with=user)
        )
        .distinct()
    )


def get_lang_user_dictionaries(user: User):
    return (
        remember_line.models.Dictionary.objects.filter(
            is_public=True, is_language=True
        )
        .filter(
            django.db.models.Q(creator=user)
            | django.db.models.Q(shared_with=user)
        )
        .distinct()
    )


def get_not_lang_user_dictionaries(user: User):
    return (
        remember_line.models.Dictionary.objects.filter(
            is_public=True, is_language=False
        )
        .filter(
            django.db.models.Q(creator=user)
            | django.db.models.Q(shared_with=user)
        )
        .distinct()
    )
