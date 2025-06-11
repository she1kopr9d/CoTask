from django.urls import path

import remember_line.views


urlpatterns = [
    path(
        "dashboard/",
        remember_line.views.dashboard_view,
        name="card_dashboard",
    ),
    path(
        "dictionary_list/",
        remember_line.views.dictionary_list_view,
        name="dictionary_list",
    ),
    path(
        "dictionary_create/",
        remember_line.views.dictionary_create_view,
        name="dictionary_create",
    ),
    path(
        "card_create/",
        remember_line.views.card_create_view,
        name="card_create",
    ),
    path(
        "review/",
        remember_line.views.card_review_next_view,
        name="card_review_next",
    ),
    path(
        'review/<int:card_id>/',
        remember_line.views.card_review_detail_view,
        name='card_review_detail'
    ),
    path(
        'cards/<int:card_id>/delete/',
        remember_line.views.card_delete,
        name='card_delete'
    ),
]
