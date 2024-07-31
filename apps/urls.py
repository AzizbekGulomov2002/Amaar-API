from django.urls import path, include

urlpatterns = [
    path('', include('apps.app.urls')),
    path('', include('apps.users.urls')),
]
