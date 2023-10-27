from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Models
from .models import (
    Product,
    Category,
    Condition
)

# Serializers
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ConditionSerializer
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
                'message': 'Product was created successfully.', 
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, id):
    try:
        product = get_object_or_404(Product, id=id)
    except Product.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        product.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    

# Condition Views
@api_view(['POST', 'GET'])
def condition_list(request):
    if request.method == "GET":
        conditions = Condition.objects.all()
        serializer = ConditionSerializer(conditions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        payload = request.data
        serializer = CategorySerializer(data=payload)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status_code': 201,
                'message': 'Condition was created successfully.', 
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def condition_details(request, id):
    try:
        condition = Condition.objects.get(id=id)
    except Condition.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        serializer = ConditionSerializer(condition, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ConditionSerializer(condition, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    if request.method == 'DELETE':
        condition.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)




# Category views
@api_view(['POST', 'GET'])
def category_list(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        payload = request.data
        serializer = CategorySerializer(data=payload)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'status_code': 201,
                'message': 'Category was created successfully.', 
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_details(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        raise Http404
    
    if request.method == 'GET':
        serializer = CategorySerializer(category, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        category.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


#  Cart data information derived from a list of product ids
@api_view(['POST'])
def get_cart_data(request):
    # The payload should be a list of number
    # sent in json format
    cart_data_ids_list = request.data
    
    if (isinstance(cart_data_ids_list, list)):
        cart_items_data = Product.objects.filter(id__in=cart_data_ids_list)
        serializer = ProductSerializer(cart_items_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({
        "detail": "invalid datatype. Must be a list or array of product ids"
    }, status=status.HTTP_400_BAD_REQUEST)

# Saved data derived from a list of product ids
@api_view(['POST'])
def get_saved_data(request):
    # The payload should be a list of ids -- int datatype
    # sent in json format
    saved_data_ids_list = request.data

    if (isinstance(saved_data_ids_list, list)):
        saved_items_data = Product.objects.filter(id__in=saved_data_ids_list)
        serializer = ProductSerializer(saved_items_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({
        "detail": "invalid datatype. Must be a list or array of product ids"
    }, status=status.HTTP_400_BAD_REQUEST)







