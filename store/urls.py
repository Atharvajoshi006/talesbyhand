# store/urls.py
from django.urls import path
from . import views
from .views import UserLoginView # For Feature 2

urlpatterns = [
    # FEATURE 1 & 3
    path('', views.home_page, name='home'),

    # FEATURE 2
    path('login/', UserLoginView.as_view(), name='login'),
    
    # FEATURE 4 (Product List by State)
    path('products/', views.product_list_by_region, name='product_list_all'),
    path('products/<str:region_slug>/', views.product_list_by_region, name='product_list_by_region'),

    # FEATURE 5 (Product Info/Detail)
    path('product/<int:product_pk>/', views.product_detail, name='product_detail'),

    # FEATURE 6 (Cart)
    path('cart/add/<int:product_pk>/', views.add_to_cart, name='add_to_cart'),
    
    # Placeholder for the cart and checkout views
    path('cart/', views.home_page, name='cart_detail'), # CHANGE ME later
    path('checkout/', views.home_page, name='checkout'), # CHANGE ME later
]