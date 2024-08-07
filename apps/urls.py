from django.urls import path, include

urlpatterns = [
    path('', include('apps.orders.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.landing.urls')),
]
