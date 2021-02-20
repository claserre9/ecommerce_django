from django.urls import path
from app_base import views

urlpatterns = [
    path('', views.home, name="app_base_home"),
    path('about/', views.about, name="app_base_about"),
    path('details/', views.product_details, name="app_base_product_details"),
]
