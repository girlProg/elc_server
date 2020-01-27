"""esteemServer URL Configuration
    yedite.ch
"""


from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view


urlpatterns = [

    path('admin/', admin.site.urls),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'api/', include('salaryapp.urls')),
    path(r'docs/', include_docs_urls(title='Esteem API')),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …"
    ), name='openapi-schema'),
]
