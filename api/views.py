from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import json

# Models
from .models import (
    Product,
    Category
)

# Serializers
from .serializers import (
    ProductSerializer
)


# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == "GET":
        
        searched_term = request.query_params.get('search')
        
        if searched_term is not None:
            products = Product.objects.filter(name__icontains=searched_term).all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        payload = request.data
        # Receives the category id from payload
        serializer = ProductSerializer(data=payload)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status_code': 201,
                'message': 'User was created successfully.', 
                'details': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)








