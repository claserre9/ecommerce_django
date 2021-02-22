from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import SignUpForm
from .models import Category, Product


def home(request, category_slug=None):
    category_page = None
    if category_slug is not None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(available=True, category=category_page)
    else:
        products = Product.objects.all().filter(available=True)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page') or "1"
    page_obj = paginator.get_page(page_number)
    return render(request, 'base/home.html',
                  {"category": category_page, "products": products, "page_obj": page_obj, 'page_number': page_number})


def product_details(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    return render(request, 'base/product_details.html', dict(product=product))


def about(request):
    return render(request, 'base/about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name="Customer")
            customer_group.user_set.add(signup_user)
            return redirect('app_base_login')
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', dict(form=form))


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'base/login.html'
    success_url = reverse_lazy('app_base_home')
    success_message = "Yeah! You are logged in"


def userlogout(request):
    logout(request)
    messages.success(request, 'Good bye !')
    return redirect('app_base_home')


def search(request):
    products = Product.objects.filter(name__icontains=request.GET['course'])
    count_result = products.count()

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page') or "1"
    page_obj = paginator.get_page(page_number)
    return render(request, 'base/home.html', dict(products=products, count_result=count_result, page_obj=page_obj, page_number=page_number))
