from django.contrib import admin
from .models import (
    Profile,
    Category,
    NewsLetter,
    Order,
    Image,
    Product,
    ShippingAddress,
    Condition
)


# Register your models here.

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(NewsLetter)
admin.site.register(Order)
admin.site.register(Image)
admin.site.register(ShippingAddress)
admin.site.register(Condition)


