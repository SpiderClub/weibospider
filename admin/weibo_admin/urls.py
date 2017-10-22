from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from . import view


urlpatterns = [
    url(r'^$', view.index),
    url(r'^admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
