from django.urls import path

from .views import RegisterView, LoginView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    # path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
]
