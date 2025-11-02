# store/models.py
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# --- 1. REGION/ARTISAN MODELS (The Tales Core) ---

class Region(models.Model):
    """The Indian State for product filtering (Feature 3)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Regions (States)"

    def __str__(self):
        return self.name

class Artisan(models.Model):
    """The creator of the product and source of the 'Tale' (Feature 5)."""
    display_name = models.CharField(max_length=255, unique=True)
    bio_story = models.TextField(help_text="The full 'Tale' of the artisan.")
    profile_image = models.ImageField(upload_to='artisan_profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.display_name

# --- 2. PRODUCT CATALOG MODELS (Features 4 & 5) ---

class Product(models.Model):
    """The item being sold."""
    artisan = models.ForeignKey(Artisan, on_delete=models.SET_NULL, null=True, related_name='products')
    region = models.ForeignKey(Region, on_delete=models.RESTRICT, related_name='products')
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ProductMedia(models.Model):
    """Images and videos for the product detail page."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(upload_to='product_media/')
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']

# --- 3. ORDERS & ACCOUNT MODELS (Features 7 & 8) ---
# ... (Address, Order, OrderItem models remain the same as defined previously)

# --- 4. TEMPORARY CART MODEL (Feature 6) ---

class Cart(models.Model):
    """Represents a customer's temporary shopping cart."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    """A single product line item within the temporary cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')
        
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"