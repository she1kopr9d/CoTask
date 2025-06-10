from django import forms
from django.contrib.auth.models import User

from social_media.models import Profile


class UserProfileForm(forms.ModelForm):
    # Добавляем поля из модели User
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    # Поля из модели Profile
    avatar = forms.ImageField(required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile  # Основная модель для формы
        fields = ['username', 'first_name', 'last_name', 'avatar', 'about']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем начальные значения для полей User
        if self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Обновляем связанный объект User
        user = profile.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()  # Сначала сохраняем User
            profile.save()  # Затем Profile
        return profile
