"""
Put viewsets in views.py only, for convinence i created a
seperate file (as views.py is already full)
"""
from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD: get post put patch delete"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = 'pk'  # default


class ProductGenericViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """get only"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = 'pk'  # default
