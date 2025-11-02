# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from .models import Region, Product, Artisan, Cart, CartItem
from django.urls import reverse

# --- FEATURE 1: Home Page & FEATURE 3: State Selection ---
def home_page(request):
    """1] Home page & 3] states: Lists all regions/states."""
    regions = Region.objects.all().order_by('name')
    context = {
        'regions': regions,
        'website_info': "Welcome to Tales by Hand: Shop authentic artisan products linked to the rich history of their Indian states.",
    }
    return render(request, 'store/home.html', context)

# --- FEATURE 2: Login ---
class UserLoginView(LoginView):
    """2] Login: Uses built-in Django view."""
    template_name = 'store/login.html'

# --- FEATURE 4: Products by State ---
def product_list_by_region(request, region_slug=None):
    """4] products: Displays products filtered by the selected state."""
    region = None
    if region_slug:
        region = get_object_or_404(Region, slug=region_slug)
        products = Product.objects.filter(region=region, is_active=True).select_related('artisan')
    else:
        # Show all products if no region is selected
        products = Product.objects.filter(is_active=True).select_related('artisan')
    
    context = {
        'region': region,
        'products': products,
    }
    return render(request, 'store/product_list.html', context)

# --- FEATURE 5: Product Info/Detail ---
def product_detail(request, product_pk):
    """5] product info: Shows product details and the Artisan's Tale."""
    product = get_object_or_404(
        Product.objects.select_related('artisan', 'region'), 
        pk=product_pk, 
        is_active=True
    )
    product_images = product.media.all()
    
    context = {
        'product': product,
        'images': product_images,
    }
    return render(request, 'store/product_detail.html', context)

# --- FEATURE 6: Cart (Add Item Logic) ---
@require_POST
@login_required # Ensure the user is logged in to manage their cart
def add_to_cart(request, product_pk):
    """Handles adding a product to the user's temporary cart."""
    product = get_object_or_404(Product, pk=product_pk)
    quantity = int(request.POST.get('quantity', 1))

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not item_created:
        # If the item exists, increase the quantity
        cart_item.quantity += quantity
        cart_item.save()

    # Redirect to the cart view (which you'll implement later)
    return redirect('cart_detail')