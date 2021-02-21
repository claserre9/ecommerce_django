from django.shortcuts import render, get_object_or_404

from .models import Category, Product


def home(request, category_slug=None):
    category_page = None
    if category_slug is not None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category_page)
    else:
        products = Product.objects.all().filter(available=True)
    return render(request, 'base/home.html', {"category": category_page, "products": products})


def product_details(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    return render(request, 'base/product_details.html', dict(product=product))


def about(request):
    return render(request, 'base/about.html')
