from django.core.exceptions import ObjectDoesNotExist

from .models import Category, Cart, CartItem


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)


def cart_infos(request):
    count_product_quantity = 0
    if request.session.exists:
        try:
            cart = Cart.objects.get(cart_id=request.session.session_key)
            cart_item = CartItem.objects.filter(cart_id=cart.id)
            for c in cart_item:
                count_product_quantity += c.quantity
        except ObjectDoesNotExist:
            pass
    return dict(count_product_quantity_session=count_product_quantity)

