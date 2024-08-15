from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import payment_success, payment_fail
from .views.infos_views import BannerViewSet, DeliveryInfoViewSet, PolicyAndPrivacyViewSet, PublicOfferViewSet, \
    ReturnPolicyViewSet, DashboardView
from .views.order_views import OrderHistoryViewSet, OrderListAPIView
from .views.product_views import CategoryViewSet, AllCategoryViewSet, ProductViewSet, BestProductsListView
from .views.user_views import UserOrderHistoryAPIView
from .views.webhook import stripe_webhook

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('all_categories', AllCategoryViewSet, basename='all_categories')
router.register('products', ProductViewSet)
router.register('banners', BannerViewSet)
router.register('delivery-info', DeliveryInfoViewSet)
router.register('policy-and-privacy', PolicyAndPrivacyViewSet)
router.register('public-offer', PublicOfferViewSet)
router.register('return-policy', ReturnPolicyViewSet)

router.register('order-history', OrderHistoryViewSet, basename='order-history')
urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', stripe_webhook, name='webhook'),
    path('best_products/', BestProductsListView.as_view(), name='best-products'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('order-history/users/<int:user_id>/', UserOrderHistoryAPIView.as_view(), name='user-order-history'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('success/', payment_success, name='payment_success'),
    path('fail/', payment_fail, name='payment_fail'),

]
