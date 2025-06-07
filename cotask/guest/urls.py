from django.urls import path

import guest.views


urlpatterns = [
    path("", guest.views.index, name="guest")
]
