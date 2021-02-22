from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
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
    return render(request, 'base/home.html', {"category": category_page, "products": products})


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


# def userlogin(request):
#     if request == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('app_base_home')
#         else:
#             return redirect("app_base_signup")
#
#         # form = AuthenticationForm(data=request.POST)
#         # print(request.POST)
#         # if form.is_valid():
#         #     username = request.POST['username']
#         #     password = request.POST['password']
#         #     print(username, password)
#         #     user = authenticate(request, username=username, password=password)
#         #     if user is not None:
#         #         login(request, user)
#         #         return redirect('app_base_home')
#         #     else:
#         #         return redirect("app_base_signup")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'base/login.html', dict(form=form))


def userlogout(request):
    logout(request)
    messages.success(request, 'Good bye !')
    return redirect('app_base_home')
