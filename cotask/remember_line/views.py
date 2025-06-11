from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden

from remember_line.models import CardReview, CardAssociation, Dictionary, Card
from remember_line.forms import DictionaryForm, CardForm

from remember_line.logic.card_service import create_dictionary
from remember_line.logic.review_service import schedule_review


@login_required
def dashboard_view(request):
    user = request.user

    # Карточки, которые нужно повторить (next_review <= сейчас)
    cards_to_review = (
        CardReview.objects
        .filter(user=user, next_review__lte=timezone.now())
        .select_related('card')
        .order_by('next_review')
    )

    # Последние ассоциации пользователя
    recent_associations = (
        CardAssociation.objects
        .filter(user=user)
        .select_related('card')
        .order_by('-created_at')[:5]
    )

    return render(request, 'remember_line/dashboard.html', {
        'cards_to_review': [review.card for review in cards_to_review],
        'recent_associations': recent_associations
    })


@login_required
def dictionary_list_view(request):
    dictionaries = Dictionary.objects.filter(creator=request.user)
    return render(
        request,
        'remember_line/dictionary_list.html',
        {
            'dictionaries': dictionaries,
        },
    )


@login_required
def dictionary_create_view(request):
    if request.method == 'POST':
        form = DictionaryForm(request.POST)
        if form.is_valid():
            create_dictionary(
                name=form.cleaned_data['name'],
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

    if request.method == 'POST':
        quality = int(request.POST.get('quality'))
        schedule_review(review, quality)
        return redirect('card_review_next')  # Перейти к следующей карточке

    return render(
        request,
        'remember_line/card_review_next.html',
        {
            'card': review.card,
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