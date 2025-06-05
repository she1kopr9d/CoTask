from django.urls import path

import user.views


urlpatterns = [
    path('login/', user.views.login_view, name="login"),
    path('reg/', user.views.signup_view, name="reg"),
]
