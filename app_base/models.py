from datetime import datetime

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
