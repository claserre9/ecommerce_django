from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def product_details(request):
    return render(request, 'base/product_details.html')


def about(request):
    return render(request, 'base/about.html')
