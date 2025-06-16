import django.forms

import remember_line.models


class DictionaryForm(django.forms.ModelForm):
    class Meta:
        model = remember_line.models.Dictionary
        fields = ["name", "is_public", "is_language"]
        labels = {
            "name": "Название словаря",
            "is_public": "Сделать словарь публичным",
            "is_language": "Это языковой словарь",
        }


class CardForm(django.forms.ModelForm):
    class Meta:
        model = remember_line.models.Card
        fields = ["dictionary", "front", "back"]
        labels = {
            "dictionary": "Словарь",
            "front": "Лицевая сторона (слово)",
            "back": "Оборотная сторона (перевод)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["dictionary"].queryset = (
                remember_line.models.Dictionary.objects.filter(creator=user)
            )
