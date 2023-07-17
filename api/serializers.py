from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'price',
            'discount',
            'quantity_available',
            'product_in_stock',
            'ratings',
            'thumbnails',
        ]





