from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Tashkent Market API",
        default_version='v1',
        description="API documentation for Tashkent Market",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@tashkentmarket.ae"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # noqa
)
from apps.users.views import UserDetailsAPIView
urlpatterns = [
    path('api/auth/user/<int:pk>/', UserDetailsAPIView.as_view(), name='user-detail'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
                   static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
