"""
create router in urls.py only [here for convenience]
"""

from rest_framework.routers import DefaultRouter

from products.viewsets import ProductGenericViewSet, ProductViewSet

router = DefaultRouter()
# router.register('products-abc', ProductViewSet, basename='products')
router.register('products-abc', ProductGenericViewSet, basename='products')

urlpatterns = router.urls
