# orders/admin.py
from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']
    fields = ['product', 'quantity', 'unit_price', 'subtotal']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at', 'updated_at', 'item_count', 'total']
    list_select_related = ['customer__user']
    search_fields = ['customer__user__username', 'customer__user__first_name', 'customer__user__last_name']
    readonly_fields = ['total']
    inlines = [CartItemInline]

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()

    def get_queryset(self, request):
        # Optimize DB queries
        return super().get_queryset(request).prefetch_related('items__product')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']
    fields = ['product', 'quantity', 'unit_price', 'subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number',
        'customer',
        'placed_at',
        'order_status',
        'payment_status',
        'shipping_method',
        'total',
        'item_count'
    ]
    list_filter = [
        'order_status',
        'payment_status',
        'placed_at',
        'shipped_at',
        'delivered_at'
    ]
    search_fields = [
        'order_number',
        'customer__user__username',
        'customer__user__first_name',
        'customer__user__last_name',
        'tracking_number'
    ]
    readonly_fields = [
        'order_number',
        'placed_at',
        'total',
        'shipped_at',
        'delivered_at'
    ]
    inlines = [OrderItemInline]
    date_hierarchy = 'placed_at'
    ordering = ['-placed_at']

    @admin.display(description="Items")
    def item_count(self, obj):
        return obj.items.count()

    @admin.display(description="Total")
    def total(self, obj):
        return f"${obj.total:.2f}"

    def get_queryset(self, request):
        # Reduce database queries
        return super().get_queryset(request).select_related(
            'customer__user', 'shipping_address'
        ).prefetch_related('items__product')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['order__order_status']
    search_fields = ['order__order_number', 'product__title']
    readonly_fields = ['subtotal']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'unit_price', 'subtotal']
    search_fields = ['cart__customer__user__username', 'product__title']
    readonly_fields = ['subtotal']