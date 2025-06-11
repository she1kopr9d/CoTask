from django.contrib import admin
from remember_line.models import Dictionary, Card, CardReview, CardAssociation


# Inline для карточек внутри словаря
class CardInline(admin.TabularInline):
    model = Card
    extra = 0


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator')
    list_filter = ('creator',)
    search_fields = ('name',)
    inlines = [CardInline]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'dictionary', 'creator')
    list_filter = ('dictionary', 'creator')
    search_fields = ('front', 'back')


@admin.register(CardAssociation)
class CardAssociationAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'text_snippet', 'created_at')
    list_filter = ('user', 'card')
    search_fields = ('text', 'example_phrase')

    def text_snippet(self, obj):
        return (obj.text[:50] + '...') if obj.text else '—'
    text_snippet.short_description = 'Текст'


@admin.register(CardReview)
class CardReviewAdmin(admin.ModelAdmin):
    list_display = ('card', 'user', 'last_reviewed', 'next_review', 'ease_factor', 'interval', 'repetitions')
    list_filter = ('user', 'card', 'next_review')
    search_fields = ('card__front', 'user__username')
