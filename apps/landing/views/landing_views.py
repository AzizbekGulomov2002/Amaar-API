# views.py
from rest_framework import viewsets
from apps.landing.models.landing import *
from apps.landing.serializers.landing_serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated

class SpecialOfferViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = SpecialOffer.objects.all()
    serializer_class = SpecialOfferSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class SocialNetworksViewSet(viewsets.ModelViewSet):
    queryset = SocialNetworks.objects.all()
    serializer_class = SocialNetworksSerializer
    

class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class RecallViewSet(viewsets.ModelViewSet):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    permission_classes = [AllowAny]

    # def perform_create(self, serializer):
    #     if self.request.user.is_authenticated:
    #         serializer.save(client=self.request.user)
    #     else:
    #         raise PermissionError("Authentication credentials were not provided.")