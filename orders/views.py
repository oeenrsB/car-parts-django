from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'unit_price': product.unit_price}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    
    return redirect('orders:cart_detail')

def cart_detail(request):
    """View shopping cart"""
    cart_items = []
    total = 0
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(customer=request.user.customer).first()
        if cart:
            cart_items = cart.items.all()
            total = cart.total
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/cart_detail.html', context)

@login_required
def checkout(request):
    """Checkout page"""
    cart = get_object_or_404(Cart, customer=request.user.customer)
    
    if request.method == 'POST':
        # Create order logic here
        pass
    
    context = {
        'cart': cart,
    }
    return render(request, 'orders/checkout.html', context)
