from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .forms import SignUpForm
from .models import Category, Product, Cart, CartItem


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
    return render(request, 'base/home.html',
                  dict(products=products, count_result=count_result, page_obj=page_obj, page_number=page_number))


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()
    return redirect('app_base_cart')


def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart_el = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_el)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'base/cart.html',
                  dict(cart_items=cart_items, total=total, counter=counter))


def remove_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('app_base_cart')


def delete_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('app_base_cart')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_configuration = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_configuration, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            cart_el = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart_el)
            line_cart_items = list()
            for cart_item in cart_items:
                line_cart_items.append(dict(name=cart_item.product.name, quantity=cart_item.quantity, currency='usd',
                                            amount=str(int(cart_item.product.price * 100))))
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=line_cart_items
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
