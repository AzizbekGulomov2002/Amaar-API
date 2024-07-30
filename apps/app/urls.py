from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'all_categories', AllCategoryViewSet, basename='all_categories')
router.register(r'products', ProductViewSet)
router.register(r'banners', BannerViewSet)


router.register(r'delivery-info', DeliveryInfoViewSet)
router.register(r'policy-and-privacy', PolicyAndPrivacyViewSet)
router.register(r'public-offer', PublicOfferViewSet)
router.register(r'return-policy', ReturnPolicyViewSet)

router.register(r'order-history', OrderHistoryViewSet, basename='order-history')
urlpatterns = [
    path('', include(router.urls)),

    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),


    path('best_products/', BestProductsListView.as_view(), name='best-products'),

    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('orders/user/<int:user_id>/', UserOrderListAPIView.as_view(), name='user-order-list'),


    path('dashboard/', DashboardView.as_view(), name='dashboard')
]
