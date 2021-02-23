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
    path('cart/', views.cart, name="app_base_cart"),
    path('logout/', views.userlogout, name="app_base_logout"),
]
