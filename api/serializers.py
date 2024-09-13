from django.conf import settings
from rest_framework import serializers

User = settings.AUTH_USER_MODEL


class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field='pk', view_name='product-detail', read_only=True)
    title = serializers.CharField(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)

    def get_other_products(self, obj):
        user = obj
        products = user.products.all()[:5]
        return UserProductInlineSerializer(products, many=True, context=self.context).data
