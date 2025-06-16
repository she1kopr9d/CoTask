import django.forms

import social_media.models


class UserProfileForm(django.forms.ModelForm):
    username = django.forms.CharField(max_length=150)
    first_name = django.forms.CharField(max_length=30, required=False)
    last_name = django.forms.CharField(max_length=150, required=False)

    avatar = django.forms.ImageField(required=False)
    about = django.forms.CharField(
        widget=django.forms.Textarea, required=False
    )

    class Meta:
        model = social_media.models.Profile
        fields = ["username", "first_name", "last_name", "avatar", "about"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields["username"].initial = self.instance.user.username
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            profile.save()
        return profile
