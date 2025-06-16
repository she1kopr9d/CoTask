import django.contrib

import remember_line.models


# Inline для карточек внутри словаря
class CardInline(django.contrib.admin.TabularInline):
    model = remember_line.models.Card
    extra = 0


@django.contrib.admin.register(remember_line.models.Dictionary)
class DictionaryAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "creator")
    list_filter = ("creator",)
    search_fields = ("name",)
    inlines = [CardInline]


@django.contrib.admin.register(remember_line.models.Card)
class CardAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("front", "back", "dictionary", "creator")
    list_filter = ("dictionary", "creator")
    search_fields = ("front", "back")


@django.contrib.admin.register(remember_line.models.CardAssociation)
class CardAssociationAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("card", "user", "text_snippet", "created_at")
    list_filter = ("user", "card")
    search_fields = ("text", "example_phrase")

    def text_snippet(self, obj):
        return (obj.text[:50] + "...") if obj.text else "—"

    text_snippet.short_description = "Текст"


@django.contrib.admin.register(remember_line.models.CardReview)
class CardReviewAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "card",
        "user",
        "last_reviewed",
        "next_review",
        "ease_factor",
        "interval",
        "repetitions",
    )
    list_filter = ("user", "card", "next_review")
    search_fields = ("card__front", "user__username")
