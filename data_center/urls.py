"""youtube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

import version

class Version(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        return Response({"version": version.__version__}) # pylint: disable=no-member

admin.autodiscover()

SCHEMA_VIEWS = get_schema_view(
    openapi.Info(
        title="youtube API",
        default_version='v1',
        description="APIs to retrieve youtube provides",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_urls = [
    path('', include('apps.youtube.urls'), name='youtube-apis')
]

apipatterns = [
    path("admin/", admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', SCHEMA_VIEWS.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', SCHEMA_VIEWS.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('health/', include('health_check.urls')),
    path("api/", include(api_urls), name="api"),
]

urlpatterns = [
    path('api/youtube/', include(apipatterns), name="all_routes"),
]
