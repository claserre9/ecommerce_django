from django.urls import path
from app_base import views

urlpatterns = [
    path('', views.home, name="app_base_home"),
    path('<str:category_slug>', views.home, name="app_base_home"),
    path('about/', views.about, name="app_base_about"),
    path('<str:category_slug>/<str:product_slug>', views.product_details, name="app_base_product_details"),
]
