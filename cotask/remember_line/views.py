from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden, Http404
from django.contrib import messages
from django.contrib.auth.models import User

from remember_line.models import CardReview, CardAssociation, Dictionary, Card
from remember_line.forms import DictionaryForm, CardForm

from remember_line.logic.card_service import create_dictionary, create_card_review
from remember_line.logic.review_service import schedule_review, add_all_review


@login_required
def dashboard_view(request):
    user = request.user

    # Получаем словари, к которым у пользователя есть доступ
    available_dictionaries = Dictionary.objects.filter(
        Q(creator=user) | Q(shared_with=user)
    ).distinct()

    # Получаем карточки из этих словарей
    accessible_card_ids = []
    for dictionary in available_dictionaries.prefetch_related('cards'):
        accessible_card_ids.extend(dictionary.cards.values_list('id', flat=True))

    # Выбираем только те карточки, которые нужно повторить и которые в доступных словарях
    cards_to_review = (
        CardReview.objects
        .filter(user=user, next_review__lte=timezone.now(), card__id__in=accessible_card_ids)
        .select_related('card')
        .order_by('next_review')
    )

    # Последние ассоциации пользователя (тоже только по доступным карточкам)
    recent_associations = (
        CardAssociation.objects
        .filter(user=user, card__id__in=accessible_card_ids)
        .select_related('card')
        .order_by('-created_at')[:5]
    )

    return render(request, 'remember_line/dashboard.html', {
        'cards_to_review': [review.card for review in cards_to_review],
        'recent_associations': recent_associations
    })


@login_required
def dictionary_list_view(request):
    user = request.user

    created_dictionaries = Dictionary.objects.filter(creator=user)
    shared_dictionaries = Dictionary.objects.filter(shared_with=user).exclude(creator=user)

    # Собираем все карточки из обоих списков, чтобы получить reviews
    all_dictionaries = created_dictionaries | shared_dictionaries
    card_ids = Card.objects.filter(dictionary__in=all_dictionaries).values_list('id', flat=True)

    card_reviews = {
        review.card_id: review
        for review in CardReview.objects.filter(user=user)
    }

    return render(
        request,
        'remember_line/dictionary_list.html',
        {
            'created_dictionaries': created_dictionaries,
            'shared_dictionaries': shared_dictionaries,
            'card_reviews': card_reviews,
        },
    )


@login_required
def dictionary_create_view(request):
    if request.method == 'POST':
        form = DictionaryForm(request.POST)
        if form.is_valid():
            create_dictionary(
                name=form.cleaned_data['name'],
                is_language=form.cleaned_data["is_language"],
                is_public=form.cleaned_data["is_public"],
                creator=request.user,
            )
            return redirect('card_dashboard')  # или в список словарей
    else:
        form = DictionaryForm()

    return render(
        request,
        'remember_line/dictionary_create.html',
        {
            'form': form,
        },
    )


@login_required
def card_create_view(request):
    if request.method == 'POST':
        form = CardForm(request.POST, user=request.user)
        if form.is_valid():
            card = form.save(commit=False)
            card.creator = request.user
            card.save()
            create_card_review(card, request.user)
            return redirect('card_dashboard')
    else:
        form = CardForm(user=request.user)

    return render(request, 'remember_line/card_create.html', {'form': form})


@login_required
def card_review_next_view(request):
    review = (
        CardReview.objects
        .filter(user=request.user, next_review__lte=timezone.now())
        .select_related('card')
        .order_by('next_review')
        .first()
    )

    if not review:
        return render(request, 'remember_line/card_review_done.html')

    associations = CardAssociation.objects.filter(
        card=review.card,
        user=request.user,
    ).select_related('user')

    if request.method == 'POST':
        quality = int(request.POST.get('quality'))
        schedule_review(review, quality)
        return redirect('card_review_next')  # Перейти к следующей карточке

    return render(
        request,
        'remember_line/card_review_next.html',
        {
            'card': review.card,
            'associations': associations,
        },
    )


@login_required
def card_review_detail_view(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    review, _ = CardReview.objects.get_or_create(user=request.user, card=card)

    if request.method == 'POST':
        quality = int(request.POST.get('quality'))
        schedule_review(review, quality)
        return redirect('card_review_next')  # Или обратно в список карточек

    return render(request, 'remember_line/card_review_detail.html', {'card': card})


@login_required
def card_delete(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    if card.dictionary.creator != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту карточку.")

    if request.method == 'POST':
        card.delete()
        return redirect('dictionary_list')  # Или на другую нужную страницу

    return redirect('dictionary_list')


@login_required
def dict_delete(request, dict_id):
    dictionary = get_object_or_404(Dictionary, id=dict_id)

    if dictionary.creator != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот словарь.")

    if request.method == 'POST':
        dictionary.delete()
        return redirect('dictionary_list')  # Или на другую нужную страницу

    return redirect('dictionary_list')


@login_required
def dictionary_edit_tags(request, pk):
    dictionary = get_object_or_404(Dictionary, pk=pk, creator=request.user)

    if request.method == 'POST':
        dictionary.name = request.POST["name"]
        dictionary.is_public = 'is_public' in request.POST
        dictionary.is_language = 'is_language' in request.POST
        dictionary.save()
        return redirect('card_dashboard')

    return render(
        request,
        'remember_line/dictionary_edit_tags.html',
        {
            'dictionary': dictionary,
        },
    )


@login_required
def dictionary_detail(request, pk):
    dictionary = get_object_or_404(Dictionary, pk=pk)

    if not dictionary.is_public and dictionary.creator != request.user:
        return render(request, "403.html", status=403)

    return render(
        request,
        "remember_line/dictionary_detail.html",
        {
            "dictionary": dictionary,
        },
    )


@login_required
def dictionary_add(request, dictionary_id):
    dictionary = get_object_or_404(Dictionary, id=dictionary_id)

    if not dictionary.is_public:
        messages.error(request, "Этот словарь не является публичным.")
        return redirect("card_dashboard")

    if request.user == dictionary.creator:
        messages.info(request, "Вы уже являетесь создателем этого словаря.")
    elif request.user in dictionary.shared_with.all():
        messages.info(request, "Словарь уже добавлен.")
    else:
        dictionary.shared_with.add(request.user)
        add_all_review(request.user, dictionary)
        messages.success(request, "Словарь успешно добавлен в вашу коллекцию.")

    return redirect("card_dashboard")


@login_required
def user_dictionaries_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = profile_user == request.user

    if is_own_profile:
        return redirect("dictionary_list")

    owned = Dictionary.objects.filter(creator=profile_user)
    shared = Dictionary.objects.filter(shared_with=profile_user).exclude(creator=profile_user)

    return render(request, 'remember_line/user_dictionaries.html', {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
        'owned_dictionaries': owned,
        'shared_dictionaries': shared,
    })


@login_required
def card_edit_view(request, pk):
    card = get_object_or_404(Card, pk=pk, creator=request.user)

    if request.method == 'POST':
        card.front = request.POST["front"]
        card.back = request.POST["back"]
        card.save()
        return redirect('card_dashboard')

    return render(
        request,
        'remember_line/card_edit.html',
        {
            'card': card,
        },
    )


@login_required
def delete_association_view(request, pk):
    association = get_object_or_404(CardAssociation, pk=pk)
    if association.user != request.user:
        return Http404()

    if request.method == "POST":
        association.delete()
        return redirect("card_review_next")


@login_required
def add_association(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    if request.method == "POST":
        text = request.POST.get("text")
        image = request.FILES.get("image")
        example_phrase = request.POST.get("example_phrase")

        association = CardAssociation.objects.create(
            card=card,
            user=request.user,
            text=text,
            image=image,
            example_phrase=example_phrase,
        )

        return redirect("card_review_next")
