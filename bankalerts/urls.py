from rest_framework import routers
from . import views
from django.conf.urls import url, include
from esteemServer import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^gtb', views.gt_parser_view , name='gtb'),
    url(r'^fb', views.fb_parser_view , name='fb'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
