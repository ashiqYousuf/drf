from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from .validators import unique_product_title, validate_title


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    a_url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk')
    title = serializers.CharField(
        validators=[validate_title, unique_product_title]
    )
    # name = serializers.CharField(source='title', read_only=True)
    # if we have user attached to the model (f.k)
    # email = serializers.EmailField(source='user.email', read_only=True)
    # email = serializers.EmailField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'pk',
            #   'user',
            'title',
            #   'name',
            'url',
            'a_url',
            'content',
            'price',
            'sale_price',
            'discount'
        ]

    # def validate_title(self, value):
    #     """
    #     field level validations
    #     """
    #     request = self.context.get('request')
    #     user = request.user

    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already taken")
    #     return value

    def create(self, validated_data):
        """
        override create method
        return Product.objects.create(**validated_data)
        """
        # email = validated_data.pop('email')
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_date):
        """
        override update method
        """
        # email = validated_date.pop('email')
        # instance.title = validated_date.get('title', instance.title)
        # instance.save()
        return super().update(instance, validated_date)

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
