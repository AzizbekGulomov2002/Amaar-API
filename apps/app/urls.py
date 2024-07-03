from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, BannerViewSet, \
    OrderDetailAPIView, OrderListAPIView, DashboardView, AllCategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'all_categories', AllCategoryViewSet, basename='all_categories')
router.register(r'products', ProductViewSet)
router.register(r'banners', BannerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderListAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard')

]
