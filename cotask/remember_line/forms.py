from django import forms
from remember_line.models import Dictionary, Card


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ['name', 'is_public', 'is_language']
        labels = {
            'name': 'Название словаря',
            'is_public': 'Сделать словарь публичным',
            'is_language': 'Это языковой словарь',
        }


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['dictionary', 'front', 'back']
        labels = {
            'dictionary': 'Словарь',
            'front': 'Лицевая сторона (слово)',
            'back': 'Оборотная сторона (перевод)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['dictionary'].queryset = Dictionary.objects.filter(creator=user)
