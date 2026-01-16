from django.contrib import admin
from .models import (
    Category, 
    Manufacturer, 
    Product, 
    ProductSpecification, 
    ProductFitment,
    ProductDocument
)


# ==================== CATEGORY ADMIN ====================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']
    list_filter = ['parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


# ==================== MANUFACTURER ADMIN ====================
@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


# ==================== INLINE ADMINS ====================
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ['name', 'value', 'unit']


class ProductFitmentInline(admin.TabularInline):
    model = ProductFitment
    extra = 1
    fields = ['vehicle', 'position', 'fitment_notes']
    autocomplete_fields = ['vehicle']


# ==================== PRODUCT ADMIN ====================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'sku',
        'category',
        'manufacturer',
        'unit_price',
        'inventory',
        'product_type',
        'is_active'
    ]
    
    list_filter = [
        'is_active',
        'product_type',
        'category',
        'manufacturer'
    ]
    
    search_fields = [
        'title',
        'sku',
        'part_number',
        'oem_part_number'
    ]
    
    prepopulated_fields = {'slug': ('title',)}
    
    autocomplete_fields = ['category', 'manufacturer']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'sku', 'description')
        }),
        ('Categorization', {
            'fields': ('category', 'manufacturer', 'product_type')
        }),
        ('Pricing & Inventory', {
            'fields': ('unit_price', 'cost_price', 'inventory', 'reorder_level')
        }),
        ('Part Details', {
            'fields': ('part_number', 'oem_part_number', 'is_universal'),
            'classes': ('collapse',)
        }),
        ('Physical Properties', {
            'fields': ('weight', 'length', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('warranty_months', 'is_active', 'is_featured')
        }),
    )
    
    inlines = [
        ProductSpecificationInline,
        ProductFitmentInline
    ]
    
    list_per_page = 50
    save_on_top = True


# ==================== PRODUCT SPECIFICATION ADMIN ====================
@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value', 'unit']
    list_filter = ['name']
    search_fields = ['product__title', 'name', 'value']
    autocomplete_fields = ['product']


# ==================== PRODUCT FITMENT ADMIN ====================
@admin.register(ProductFitment)
class ProductFitmentAdmin(admin.ModelAdmin):
    list_display = ['product', 'vehicle', 'position']
    list_filter = ['position']
    search_fields = [
        'product__title',
        'vehicle__model__name',
        'vehicle__model__make__name'
    ]
    autocomplete_fields = ['product', 'vehicle']