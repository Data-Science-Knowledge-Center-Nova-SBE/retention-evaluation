from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from webapi import settings

admin.site.site_header = 'Retention Evaluation Admin'

schema_view = get_schema_view(
  openapi.Info(
    title="API",
    default_version='v1',
    description="",
    contact=openapi.Contact(email="datascience@novasbe.pt")
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
  # admin
  path('config/', admin.site.urls),

  # site
  path('authsite/', include('apps.web.authsite.urls')),
  path('', include('apps.web.management.urls')),

  # api modules
  path('api/modeling/', include('apps.api.modeling.urls')),
  path('api/history/', include('apps.api.history.urls')),

  # docs
  url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
