from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    a_url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk')

    class Meta:
        model = Product
        fields = ['pk', 'title', 'url', 'a_url', 'content',
                  'price', 'sale_price', 'discount']

    def get_discount(self, obj):
        """
        when we use serializer method field it assumes that an obj is actual instance when 
        we do serializer.save() else it's data passed (dict) and obj.get_discount() raises an error.
        """
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-detail", kwargs={"pk": obj.pk}, request=request)
