from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.landing.serializers.landing_serializers import *


class SpecialOfferViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer


class SocialNetworksViewSet(viewsets.ModelViewSet):
    queryset = SocialNetworks.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SocialNetworksSerializer


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class RecallViewSet(viewsets.ModelViewSet):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    permission_classes = [IsAuthenticated]


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = [IsAuthenticated]
