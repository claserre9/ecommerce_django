import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def instant_directory_path_for_category(instance, filename):
    file_name, extension = filename.split(".")
    dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
    file_name = dt_string + "." + extension
    return f"category/{file_name}"


def instant_directory_path_for_product(instance, filename):
    file_name, extension = filename.split(".")
    dt_string = datetime.now().strftime("%d%m%Y%H%M%S")
    file_name = dt_string + "." + extension
    return f"product/{file_name}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=instant_directory_path_for_category, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('app_base_home', args=[self.slug])

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=instant_directory_path_for_product, blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_url(self):
        return reverse('app_base_product_details', args=[self.category.slug, self.slug])

    def __str__(self):
        return f"{self.name}"


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return f"{self.cart_id}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product}"


class Order(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    total = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Order total')
    email_address = models.EmailField(max_length=255, blank=True, verbose_name='Email address')
    created = models.DateTimeField(auto_now_add=True)
    shipping_name = models.CharField(max_length=255, blank=True)
    shipping_address = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=255, blank=True)
    shipping_country = models.CharField(max_length=255, blank=True)
    shipping_postal_code = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Order"
        ordering = ["-created"]

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='USD Price')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = "OrderItem"

    def sub_total(self):
        return self.price * self.quantity

    def __str__(self):
        return self.product
