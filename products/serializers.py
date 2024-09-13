from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer

from .models import Product
from .validators import unique_product_title, validate_title


class ProductSerializer(serializers.ModelSerializer):
    """
    source:- uses methods or properties of the model to generate values
    for the serialized output.
    """
    owner = UserPublicSerializer(source='user', read_only=True)
    discount = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    a_url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk', read_only=True)
    title = serializers.CharField(
        validators=[validate_title, unique_product_title]
    )
    # user_data = serializers.SerializerMethodField(read_only=True)
    # name = serializers.CharField(source='title', read_only=True)
    # if we have user attached to the model (f.k)
    # email = serializers.EmailField(source='user.email', read_only=True)
    # email = serializers.EmailField(write_only=True)
    # change field name [content -> body]
    body = serializers.CharField(source='content')
    api_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Product
        fields = [
            'pk',
            'owner',
            # 'user_data',
            'title',
            'public',
            #   'name',
            'url',
            'a_url',
            'body',
            # 'content',
            'price',
            'sale_price',
            'discount',
            'path',
            'api_url',
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

    # def get_user_data(self, obj):
    #     return {"username": obj.user.username}

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
