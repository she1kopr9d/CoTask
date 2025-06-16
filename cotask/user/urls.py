import django.urls
import django.contrib.auth.views

import user.views


urlpatterns = [
    django.urls.path("login/", user.views.login_view, name="login"),
    django.urls.path("reg/", user.views.signup_view, name="reg"),
    django.urls.path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(),
        name="logout",
    ),
]
