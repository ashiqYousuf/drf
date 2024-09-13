from rest_framework import generics
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

from . import client


class SearchListView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response({}, status=404)
        results = client.perform_search(query, tags=tag)
        return Response(results)


class OldSearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = self.request.user if self.request.user.is_authenticated else None
            print(user)
            results = qs.search(q, user=user)
        return results
