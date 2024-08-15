from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.landing.views.landing_views import *

router = DefaultRouter()
router.register('special-offers', SpecialOfferViewSet)
router.register('news', NewsViewSet)
router.register('companies', CompanyViewSet)
router.register('social-networks', SocialNetworksViewSet)
router.register('recalls', RecallViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
