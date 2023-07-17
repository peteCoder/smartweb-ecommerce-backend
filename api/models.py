from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# Create your models here.


def upload_file_to(instance, filename):
    model = instance.album.__class__._meta
    name = model.verbose_name_plural.replace(" ", "_")
    return f'{name}/images/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        related_name="user_profile", 
        on_delete=models.CASCADE, 
        null=False, blank=False
    )

    class Meta:
        verbose_name_plural = "Profiles"
        verbose_name = "Profile"

    def __str__(self) -> str:
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()

    
class ProductsProperties(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Product Property Name", 
        blank=False, null=False
    )
    value = models.CharField(
        max_length=100, 
        verbose_name="Product Property Value", 
        blank=False, null=False
    )

    class Meta:
        verbose_name_plural = "Product Properties"
        verbose_name = "Product Property"

    def __str__(self) -> str:
        return f"{self.property_name} | {self.property_value}"




class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Category Name", 
        blank=False, null=False
    )
    category_banner_image = models.ImageField(
        upload_to='category/', 
        blank=False, null=False, 
        verbose_name="Category Banner Image"
    )
    category_thumbnail_image = models.ImageField(
        upload_to='category/', 
        blank=True, null=True, 
        verbose_name="Category Thumbnail Image"
    )

    properties = models.ManyToManyField(
        ProductsProperties, 
        related_name="category_properties",
        blank=True
    )

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self) -> str:
        return self.name



class Product(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Product Name", 
        blank=False, null=False
    )
    category = models.ForeignKey(
        Category, 
        related_name="products", 
        on_delete=models.CASCADE, 
        blank=False, null=False
    )

    description = models.TextField(
        verbose_name="Product Description", 
        blank=False, null=False
    )
    price = models.BigIntegerField(default=0)
    discount = models.BigIntegerField(default=0)
    quantity_available = models.IntegerField(default=0)
    product_in_stock = models.BooleanField(default=False)
    ratings = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"

    # Helper methods
    @property
    def thumbnails(self):
        images_url_list = [album.image.url for album in self.album.images.all()]
        return images_url_list
    

    def __str__(self) -> str:
        return self.name


class ImageAlbum(models.Model):
    name = models.CharField(max_length=100, verbose_name="photo album")
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="album")

    class Meta:
        verbose_name_plural = "Image Albums"
        verbose_name = "Image Album"

    def __str__(self) -> str:
        return self.name


# Create an Album for a particular Product
@receiver(post_save, sender=Product)
def create_album(sender, created, instance, **kwargs):
    if created:
        ImageAlbum.objects.create(product=instance, name=instance.name)

@receiver(post_save, sender=Product)
def save_album(sender, instance, **kwargs):
    instance.album.save()


class Image(models.Model):
    name = models.CharField(max_length=100)
    album = models.ForeignKey(
        ImageAlbum, 
        related_name="images",
        verbose_name="Product",
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=upload_file_to, 
        blank=False, null=False, 
        verbose_name="Product image"
    )

    class Meta:
        verbose_name_plural = "Images"
        verbose_name = "Image"
    def __str__(self) -> str:
        return self.name


class ShippingAddress(models.Model):
    first_name = models.CharField(
        max_length=100, 
        verbose_name="Customer First Name", 
        blank=False, null=False
    )
    last_name = models.CharField(
        max_length=100, 
        verbose_name="Customer Last Name", 
        blank=False, null=False
    )
    country = models.CharField(
        max_length=100, 
        verbose_name="Country", 
        blank=False, null=False
    )
    state = models.CharField(
        max_length=100, 
        verbose_name="State", 
        blank=False, null=False
    )
    postal_code = models.CharField(
        max_length=100, 
        verbose_name="Zip code", 
        blank=False, null=False
    )
    address_one = models.CharField(
        max_length=100, 
        verbose_name="Address 1", 
        blank=False, null=False
    )
    address_two = models.CharField(
        max_length=100, 
        verbose_name="Address 2", 
        blank=False, null=False
    )

    class Meta:
        verbose_name_plural = "Shipping Addresses"
        verbose_name = "Shipping Address"

    def __str__(self) -> str:
        return f"CUSTOMER: {self.first_name} {self.last_name}"



class Order(models.Model):
    product = models.ForeignKey(
        Product, 
        related_name="ordered_product", 
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()
    customer = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Orders"
        verbose_name = "Order"

    def __str__(self) -> str:
        return f"{self.customer.first_name} {self.customer.last_name} ordered {self.product.name}"



class NewsLetter(models.Model):
    email = models.EmailField(max_length=100, 
        verbose_name="Customer Email Address", 
        blank=False, null=False
    )

    class Meta:
        verbose_name_plural = "Newsletters"
        verbose_name = "Newsletter"

    def __str__(self) -> str:
        return self.email











