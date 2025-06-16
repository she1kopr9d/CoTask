import django.db.models
import django.shortcuts
import django.contrib.auth.decorators
import django.utils.timezone
import django.http
import django.contrib.messages
import django.contrib.auth.models

import remember_line.models
import remember_line.forms
import remember_line.logic.card_service
import remember_line.logic.review_service


@django.contrib.auth.decorators.login_required
def dashboard_view(request):
    user = request.user

    available_dictionaries = remember_line.models.Dictionary.objects.filter(
        django.db.models.Q(creator=user) | django.db.models.Q(shared_with=user)
    ).distinct()

    accessible_card_ids = []
    for dictionary in available_dictionaries.prefetch_related("cards"):
        accessible_card_ids.extend(
            dictionary.cards.values_list("id", flat=True)
        )

    cards_to_review = (
        remember_line.models.CardReview.objects.filter(
            user=user,
            next_review__lte=django.utils.timezone.now(),
            card__id__in=accessible_card_ids,
        )
        .select_related("card")
        .order_by("next_review")
    )

    recent_associations = (
        remember_line.models.CardAssociation.objects.filter(
            user=user, card__id__in=accessible_card_ids
        )
        .select_related("card")
        .order_by("-created_at")[:5]
    )

    return django.shortcuts.render(
        request,
        "remember_line/dashboard.html",
        {
            "cards_to_review": [review.card for review in cards_to_review],
            "recent_associations": recent_associations,
        },
    )


@django.contrib.auth.decorators.login_required
def dictionary_list_view(request):
    user = request.user

    created_dictionaries = remember_line.models.Dictionary.objects.filter(
        creator=user
    )
    shared_dictionaries = remember_line.models.Dictionary.objects.filter(
        shared_with=user
    ).exclude(creator=user)

    card_reviews = {
        review.card_id: review
        for review in remember_line.models.CardReview.objects.filter(user=user)
    }

    return django.shortcuts.render(
        request,
        "remember_line/dictionary_list.html",
        {
            "created_dictionaries": created_dictionaries,
            "shared_dictionaries": shared_dictionaries,
            "card_reviews": card_reviews,
        },
    )


@django.contrib.auth.decorators.login_required
def dictionary_create_view(request):
    if request.method == "POST":
        form = remember_line.forms.DictionaryForm(request.POST)
        if form.is_valid():
            remember_line.logic.card_service.create_dictionary(
                name=form.cleaned_data["name"],
                is_language=form.cleaned_data["is_language"],
                is_public=form.cleaned_data["is_public"],
                creator=request.user,
            )
            return django.shortcuts.redirect("card_dashboard")
    else:
        form = remember_line.forms.DictionaryForm()

    return django.shortcuts.render(
        request,
        "remember_line/dictionary_create.html",
        {
            "form": form,
        },
    )


@django.contrib.auth.decorators.login_required
def card_create_view(request):
    if request.method == "POST":
        form = remember_line.forms.CardForm(request.POST, user=request.user)
        if form.is_valid():
            card = form.save(commit=False)
            card.creator = request.user
            card.save()
            remember_line.logic.card_service.create_card_review(
                card, request.user
            )
            return django.shortcuts.redirect("card_dashboard")
    else:
        form = remember_line.forms.CardForm(user=request.user)

    return django.shortcuts.render(
        request, "remember_line/card_create.html", {"form": form}
    )


@django.contrib.auth.decorators.login_required
def card_review_next_view(request):
    review = (
        remember_line.models.CardReview.objects.filter(
            user=request.user, next_review__lte=django.utils.timezone.now()
        )
        .select_related("card")
        .order_by("next_review")
        .first()
    )

    if not review:
        return django.shortcuts.render(
            request, "remember_line/card_review_done.html"
        )

    associations = remember_line.models.CardAssociation.objects.filter(
        card=review.card,
        user=request.user,
    ).select_related("user")

    if request.method == "POST":
        quality = int(request.POST.get("quality"))
        remember_line.logic.review_service.schedule_review(review, quality)
        return django.shortcuts.redirect(
            "card_review_next"
        )  # Перейти к следующей карточке

    return django.shortcuts.render(
        request,
        "remember_line/card_review_next.html",
        {
            "card": review.card,
            "associations": associations,
        },
    )


@django.contrib.auth.decorators.login_required
def card_review_detail_view(request, card_id):
    card = django.shortcuts.get_object_or_404(
        remember_line.models.Card, id=card_id
    )
    review, _ = remember_line.models.CardReview.objects.get_or_create(
        user=request.user, card=card
    )

    if request.method == "POST":
        quality = int(request.POST.get("quality"))
        remember_line.logic.review_service.schedule_review(review, quality)
        return django.shortcuts.redirect(
            "card_review_next"
        )  # Или обратно в список карточек

    return django.shortcuts.render(
        request, "remember_line/card_review_detail.html", {"card": card}
    )


@django.contrib.auth.decorators.login_required
def card_delete(request, card_id):
    card = django.shortcuts.get_object_or_404(
        remember_line.models.Card, id=card_id
    )

    if card.dictionary.creator != request.user:
        return django.http.HttpResponseForbidden(
            "Вы не можете удалить эту карточку."
        )

    if request.method == "POST":
        card.delete()
        return django.shortcuts.redirect(
            "dictionary_list"
        )  # Или на другую нужную страницу

    return django.shortcuts.redirect("dictionary_list")


@django.contrib.auth.decorators.login_required
def dict_delete(request, dict_id):
    dictionary = django.shortcuts.get_object_or_404(
        remember_line.models.Dictionary, id=dict_id
    )

    if dictionary.creator != request.user:
        return django.http.HttpResponseForbidden(
            "Вы не можете удалить этот словарь."
        )

    if request.method == "POST":
        dictionary.delete()
        return django.shortcuts.redirect("dictionary_list")

    return django.shortcuts.redirect("dictionary_list")


@django.contrib.auth.decorators.login_required
def dictionary_edit_tags(request, pk):
    dictionary = django.shortcuts.get_object_or_404(
        remember_line.models.Dictionary, pk=pk, creator=request.user
    )

    if request.method == "POST":
        dictionary.name = request.POST["name"]
        dictionary.is_public = "is_public" in request.POST
        dictionary.is_language = "is_language" in request.POST
        dictionary.save()
        return django.shortcuts.redirect("card_dashboard")

    return django.shortcuts.render(
        request,
        "remember_line/dictionary_edit_tags.html",
        {
            "dictionary": dictionary,
        },
    )


@django.contrib.auth.decorators.login_required
def dictionary_detail(request, pk):
    dictionary = django.shortcuts.get_object_or_404(
        remember_line.models.Dictionary, pk=pk
    )

    if not dictionary.is_public and dictionary.creator != request.user:
        return django.shortcuts.render(request, "403.html", status=403)

    return django.shortcuts.render(
        request,
        "remember_line/dictionary_detail.html",
        {
            "dictionary": dictionary,
        },
    )


@django.contrib.auth.decorators.login_required
def dictionary_add(request, dictionary_id):
    dictionary = django.shortcuts.get_object_or_404(
        remember_line.models.Dictionary, id=dictionary_id
    )

    if not dictionary.is_public:
        django.contrib.messages.error(
            request, "Этот словарь не является публичным."
        )
        return django.shortcuts.redirect("card_dashboard")

    if request.user == dictionary.creator:
        django.contrib.messages.info(
            request, "Вы уже являетесь создателем этого словаря."
        )
    elif request.user in dictionary.shared_with.all():
        django.contrib.messages.info(request, "Словарь уже добавлен.")
    else:
        dictionary.shared_with.add(request.user)
        remember_line.logic.review_service.add_all_review(
            request.user, dictionary
        )
        django.contrib.messages.success(
            request, "Словарь успешно добавлен в вашу коллекцию."
        )

    return django.shortcuts.redirect("card_dashboard")


@django.contrib.auth.decorators.login_required
def user_dictionaries_view(request, username):
    profile_user = django.shortcuts.get_object_or_404(
        django.contrib.auth.models.User, username=username
    )
    is_own_profile = profile_user == request.user

    if is_own_profile:
        return django.shortcuts.redirect("dictionary_list")

    owned = remember_line.models.Dictionary.objects.filter(
        creator=profile_user
    )
    shared = remember_line.models.Dictionary.objects.filter(
        shared_with=profile_user
    ).exclude(creator=profile_user)

    return django.shortcuts.render(
        request,
        "remember_line/user_dictionaries.html",
        {
            "profile_user": profile_user,
            "is_own_profile": is_own_profile,
            "owned_dictionaries": owned,
            "shared_dictionaries": shared,
        },
    )


@django.contrib.auth.decorators.login_required
def card_edit_view(request, pk):
    card = django.shortcuts.get_object_or_404(
        remember_line.models.Card, pk=pk, creator=request.user
    )

    if request.method == "POST":
        card.front = request.POST["front"]
        card.back = request.POST["back"]
        card.save()
        return django.shortcuts.redirect("card_dashboard")

    return django.shortcuts.render(
        request,
        "remember_line/card_edit.html",
        {
            "card": card,
        },
    )


@django.contrib.auth.decorators.login_required
def delete_association_view(request, pk):
    association = django.shortcuts.get_object_or_404(
        remember_line.models.CardAssociation, pk=pk
    )
    if association.user != request.user:
        return django.http.Http404()

    if request.method == "POST":
        association.delete()
        return django.shortcuts.redirect("card_review_next")


@django.contrib.auth.decorators.login_required
def add_association(request, card_id):
    card = django.shortcuts.get_object_or_404(
        remember_line.models.Card, id=card_id
    )
    if request.method == "POST":
        text = request.POST.get("text")
        image = request.FILES.get("image")
        example_phrase = request.POST.get("example_phrase")

        remember_line.models.CardAssociation.objects.create(
            card=card,
            user=request.user,
            text=text,
            image=image,
            example_phrase=example_phrase,
        )

        return django.shortcuts.redirect("card_review_next")
