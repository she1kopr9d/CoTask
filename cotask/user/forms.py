import django.forms
import django.contrib.auth.forms
import django.contrib.auth.models


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        max_length=254,
        required=True,
        widget=django.forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    first_name = django.forms.CharField(
        max_length=30,
        required=True,
        widget=django.forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = django.forms.CharField(
        max_length=30,
        required=True,
        widget=django.forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = django.contrib.auth.models.User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            "username": django.forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget = django.forms.PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["password2"].widget = django.forms.PasswordInput(
            attrs={"class": "form-control"}
        )


class LoginForm(django.contrib.auth.forms.AuthenticationForm):
    username = django.forms.CharField(
        widget=django.forms.TextInput(attrs={"class": "form-control"})
    )
    password = django.forms.CharField(
        widget=django.forms.PasswordInput(attrs={"class": "form-control"})
    )
