from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.infos_views import BannerViewSet, DeliveryInfoViewSet, PolicyAndPrivacyViewSet, PublicOfferViewSet, \
    ReturnPolicyViewSet, DashboardView
from .views.order_views import OrderHistoryViewSet, OrderListAPIView, OrderDetailAPIView
from .views.payment_views import CreatePaymentView, PaymentLinkViewSet
from .views.product_views import CategoryViewSet, AllCategoryViewSet, ProductViewSet, BestProductsListView, \
    ProductImageCreateView
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

router.register(r'order-history', OrderHistoryViewSet, basename='order-history')
urlpatterns = [
    path('', include(router.urls)),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('webhook/', stripe_webhook, name='webhook'),
    path('get_payment_link/', PaymentLinkViewSet.as_view(), name='get_payment_link'),
    path('best_products/', BestProductsListView.as_view(), name='best-products'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('order-history/users/<int:user_id>/', UserOrderHistoryAPIView.as_view(), name='user-order-history'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('product-images/', ProductImageCreateView.as_view(), name='product-image-create'),

]
