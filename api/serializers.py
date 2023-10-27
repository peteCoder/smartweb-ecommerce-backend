from rest_framework import serializers
from .models import Product, Category, Condition


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'category_details',
            'condition_details',
            'properties',
            'description',
            'price',
            'discount',
            'quantity_available',
            'product_in_stock',
            'ratings',
            'thumbnails',
            'previous_price',
            'free_shipping',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_banner_image',
            'category_thumbnail_image',
            'properties',
            'products',
        ]

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = [
            'id',
            'name',
        ]


