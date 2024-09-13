from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'sale_price', 'discount']

    def get_discount(self, obj):
        """
        when we use serializer method field it assumes that an obj is actual instance when 
        we do serializer.save() else it's data passed (dict) and obj.get_discount() raises an error.
        """
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
