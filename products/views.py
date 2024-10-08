from django.shortcuts import get_object_or_404
from rest_framework import authentication, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin, UserQuerysetMixin

from .models import Product
from .serializers import ProductSerializer

# NOTE:- Generic API Views


class ProductListCreateAPIView(StaffEditorPermissionMixin, UserQuerysetMixin, generics.ListCreateAPIView):
    # user_field = 'owner'
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication, TokenAuthentication]
    allow_staff_view = False
    # user_field = 'owner'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # django-model-perms applies to GET PUT DELETE methods only (override | custom perms)
    # permission_classes = [permissions.DjangoModelPermissions]
    # permission_classes = [IsStaffEditorPermission]

    def perform_create(self, serializer):
        # instance = serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content', None)
        if not content:
            content = title
        # we don't need user field in serializers now!
        serializer.save(content=content, user=self.request.user)
        # send signals

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     return qs.filter(user=self.request.user)


class ProductRetrieveUpdateDestroyAPIView(StaffEditorPermissionMixin, UserQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication, TokenAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]
    # permission_classes = [IsStaffEditorPermission]

    lookup_field = 'pk'

    def perform_update(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if not content:
            content = title
        serializer.save(content=content)
        # instance.content = instance.content or instance.title
        # instance.save()

    def perform_destroy(self, instance):
        # super().perform_destroy(instance)
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.status_code = 200
        response.data = {"message": "Product deleted!"}
        return response


# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'


# NOTE:- Mixin classes

"""
CreateAPIView(CreateModelMixin, GenericAPIView)
"""


class ProductMixinView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        """
        Method: GET
        """
        pk = kwargs.get('pk', None)
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if not content:
            content = "Some Fixed Content :("
        serializer.save(content=content)

# NOTE:- Function Based API View


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    """
    List, Create, Detail APIs using Func based Api Views
    """
    match request.method:
        case "GET":
            if pk is not None:
                instance = get_object_or_404(Product, pk=pk)
                data = ProductSerializer(instance, many=False).data
                return Response(data)
            qs = Product.objects.all()
            data = ProductSerializer(qs, many=True).data
            return Response(data)
        case "POST":
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content', title)
            serializer.save(content=content)
            return Response(serializer.data)
