import django.contrib.auth
import django.shortcuts

import user.forms
import user.logic.profile


def signup_view(request):
    if request.method == "POST":
        form = user.forms.SignUpForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            user.logic.profile.create_profile(user)
            django.contrib.auth.login(request, user_obj)
            return django.shortcuts.redirect("guest")
    else:
        form = user.forms.SignUpForm()
    return django.shortcuts.render(request, "user/reg.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = user.forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_obj = django.contrib.auth.authenticate(
                username=username, password=password
            )
            if user is not None:
                django.contrib.auth.login(request, user_obj)
                return django.shortcuts.redirect("guest")
    else:
        form = user.forms.LoginForm()
    return django.shortcuts.render(request, "user/login.html", {"form": form})
