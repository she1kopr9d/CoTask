import django.urls

import guest.views


urlpatterns = [django.urls.path("", guest.views.index, name="guest")]
