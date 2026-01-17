from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    """Homepage with featured products"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.filter(parent=None)
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)

def product_list(request):
    """All products with filtering"""
    products = Product.objects.filter(is_active=True)
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Filter by vehicle (if customer has selected one)
    if request.session.get('selected_vehicle_id'):
        vehicle_id = request.session['selected_vehicle_id']
        products = products.filter(fitments__vehicle_id=vehicle_id).distinct()
    
    context = {
        'products': products,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Check if fits customer's vehicle
    fits_vehicle = False
    if request.session.get('selected_vehicle_id'):
        vehicle_id = request.session['selected_vehicle_id']
        fits_vehicle = product.fitments.filter(vehicle_id=vehicle_id).exists()
    
    context = {
        'product': product,
        'fits_vehicle': fits_vehicle,
        'specifications': product.specifications.all(),
        'images': product.images.all(),
    }
    return render(request, 'products/product_detail.html', context)