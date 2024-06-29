
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import RegisterView, LoginView, CompanyListCreateView, CompanyDetailView, UserListCreateAPIView, \
    UserDetailsAPIView

# router = SimpleRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),

    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailsAPIView.as_view(), name='user-details'),
]