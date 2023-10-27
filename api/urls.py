from django.urls import path
from .views import (
    product_list,
    category_list,
    get_cart_data,
    product_details,
    category_details,
    get_saved_data,
    condition_list,
    condition_details
)

urlpatterns = [
    path('product/', product_list, name="product_list"),
    path('product/<int:id>/', product_details, name="product_details"),
    path('category/', category_list, name="category_list"),
    path('category/<int:id>/', category_details, name="category_details"),
    path('condition/', condition_list, name="condition_list"),
    path('condition/<int:id>/', condition_details, name="condition_details"),
    path('cart/', get_cart_data, name="get_cart_data"),
    path('saved/', get_saved_data, name="get_saved_data"),
]

