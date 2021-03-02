from django.urls import path
from app_base import views

urlpatterns = [
    path('', views.home, name="app_base_home"),
    path('category/<str:category_slug>', views.home, name="app_base_home"),
    path('about/', views.about, name="app_base_about"),
    path('category/<str:category_slug>/<str:product_slug>', views.product_details, name="app_base_product_details"),
    path('signup/', views.signup, name="app_base_signup"),
    path('login/', views.LoginUserView.as_view(), name="app_base_login"),
    path('search/', views.search, name="app_base_search"),
    path('cart/', views.cart_detail, name="app_base_cart"),
    path('cart/add/<int:product_id>', views.add_cart, name="app_base_add_cart"),
    path('cart/remove/<int:product_id>', views.remove_cart, name="app_base_remove_cart"),
    path('cart/delete/<int:cart_item_id>', views.delete_item, name='app_base_delete_item'),
    path('create-checkout-session', views.create_checkout_session, name='app_base_create_checkout_session'),
    path('success/', views.payment_success, name="app_base_success_payment"),
    path('cancelled/', views.CancelledView.as_view()),
    path('order-history/', views.order_history, name="app_base_order_history"),
    path('order-details/<int:order_id>', views.order_details, name="app_base_order_details"),
    path('logout/', views.userlogout, name="app_base_logout"),
]
