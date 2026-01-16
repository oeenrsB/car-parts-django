from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Make, Model, Vehicle


@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'model_count']
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    
    def model_count(self, obj):
        count = obj.models.count()
        return format_html('<b style="color: #007bff;">{}</b> models', count)
    model_count.short_description = 'Total Models'
    
    def get_queryset(self, request):
        """Optimize queries"""
        qs = super().get_queryset(request)
        return qs.annotate(models_count=Count('models'))


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'make_link', 'slug', 'vehicle_count']
    list_filter = ['make']
    search_fields = ['name', 'make__name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['make']
    ordering = ['make__name', 'name']
    
    def make_link(self, obj):
        """Clickable make name"""
        return format_html(
            '<a href="/admin/vehicles/make/{}/change/">{}</a>',
            obj.make.id,
            obj.make.name
        )
    make_link.short_description = 'Make'
    
    def vehicle_count(self, obj):
        count = obj.vehicles.count()
        color = 'green' if count > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} years</span>',
            color, count
        )
    vehicle_count.short_description = 'Years Available'


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = [
        'display_name',
        'year',
        'get_make',
        'get_model_name',
        'trim',
        'engine',
        'body_type',
        # 'parts_count'
    ]
    
    list_filter = [
        'year',
        'model__make',
        'body_type',
        'trim'
    ]
    
    search_fields = [
        'model__name',
        'model__make__name',
        'year',
        'trim',
        'engine'
    ]
    
    autocomplete_fields = ['model']
    
    fieldsets = (
        ('Vehicle Information', {
            'fields': ('model', 'year')
        }),
        ('Specifications', {
            'fields': ('trim', 'engine', 'body_type'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-year', 'model__make__name', 'model__name', 'trim']
    list_per_page = 50
    
    def display_name(self, obj):
        icon = '🚗'
        if obj.body_type == 'SUV':
            icon = '🚙'
        elif obj.body_type == 'Truck':
            icon = '🚚'
        return format_html('{} <b>{}</b>', icon, str(obj))
    display_name.short_description = 'Vehicle'
    
    def get_make(self, obj):
        return obj.model.make.name
    get_make.short_description = 'Make'
    get_make.admin_order_field = 'model__make__name'
    
    def get_model_name(self, obj):
        return obj.model.name
    get_model_name.short_description = 'Model'
    get_model_name.admin_order_field = 'model__name'
    
    # def parts_count(self, obj):
    #     count = obj.compatible_products.count()
    #     if count > 20:
    #         color = 'green'
    #     elif count > 0:
    #         color = 'orange'
    #     else:
    #         color = 'red'
        
    #     return format_html(
    #         '<span style="color: {}; font-weight: bold;">{}</span>',
    #         color, count
    #     )
    # parts_count.short_description = 'Parts'
    
    # def get_queryset(self, request):
    #     """Optimize database queries"""
    #     qs = super().get_queryset(request)
    #     return qs.select_related('model', 'model__make').annotate(
    #         parts_count=Count('compatible_products')
    #     )
