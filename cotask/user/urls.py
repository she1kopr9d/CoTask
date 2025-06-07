from django.urls import path
from django.contrib.auth.views import LogoutView

import user.views


urlpatterns = [
    path('login/', user.views.login_view, name="login"),
    path('reg/', user.views.signup_view, name="reg"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
