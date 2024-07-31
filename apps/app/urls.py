from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('all_categories', AllCategoryViewSet, basename='all_categories')
router.register('products', ProductViewSet)
router.register('banners', BannerViewSet)
router.register('delivery-info', DeliveryInfoViewSet)
router.register('policy-and-privacy', PolicyAndPrivacyViewSet)
router.register('public-offer', PublicOfferViewSet)
router.register('return-policy', ReturnPolicyViewSet)


router.register(r'order-history', OrderHistoryViewSet, basename='order-history')
urlpatterns = [
    path('', include(router.urls)),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('get_payment_link/', PaymentLinkViewSet.as_view(), name='get_payment_link'),
    path('best_products/', BestProductsListView.as_view(), name='best-products'),
    path('best_products/', BestProductsListView.as_view(), name='best-products'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('order-history/users/<int:user_id>/', UserOrderHistoryAPIView.as_view(), name='user-order-history'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')
]
