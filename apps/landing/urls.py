# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.landing.views.landing_views import *

router = DefaultRouter()
router.register(r'special-offers', SpecialOfferViewSet)
router.register(r'news', NewsViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'recalls', RecallViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
