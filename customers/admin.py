from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Address, CustomerVehicle


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('street', 'city', 'is_default')


class CustomerVehicleInline(admin.TabularInline):
    model = CustomerVehicle
    extra = 0
    fields = ('vehicle', 'nickname', 'is_primary', 'vin', 'mileage', 'purchase_date')
    autocomplete_fields = ['vehicle']
    readonly_fields = ('added_at',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user', 'email', 'phone', 'membership', 'get_vehicle_count', 'get_address_count')
    list_filter = ('membership',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'email', 'phone')
    autocomplete_fields = ['user']
    inlines = [AddressInline, CustomerVehicleInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Membership', {
            'fields': ('membership',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" or obj.user.username
    get_full_name.short_description = 'Name'
    
    def get_vehicle_count(self, obj):
        count = obj.vehicles.count()
        return format_html('<span style="color: #0066cc;">{}</span>', count)
    get_vehicle_count.short_description = 'Vehicles'
    
    def get_address_count(self, obj):
        count = obj.addresses.count()
        return format_html('<span style="color: #0066cc;">{}</span>', count)
    get_address_count.short_description = 'Addresses'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'street', 'city', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('customer__user__username', 'customer__user__first_name', 'customer__user__last_name', 'street', 'city')
    autocomplete_fields = ['customer']
    
    fieldsets = (
        ('Customer', {
            'fields': ('customer',)
        }),
        ('Address Details', {
            'fields': ('street', 'city', 'is_default')
        }),
    )


@admin.register(CustomerVehicle)
class CustomerVehicleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'vehicle', 'nickname', 'is_primary', 'vin', 'mileage', 'added_at')
    list_filter = ('is_primary', 'added_at')
    search_fields = ('customer__user__username', 'customer__user__first_name', 'customer__user__last_name', 
                    'vehicle__make__name', 'vehicle__model__name', 'nickname', 'vin')
    autocomplete_fields = ['customer', 'vehicle']
    readonly_fields = ('added_at',)
    date_hierarchy = 'added_at'
    
    fieldsets = (
        ('Customer & Vehicle', {
            'fields': ('customer', 'vehicle', 'nickname')
        }),
        ('Vehicle Details', {
            'fields': ('vin', 'mileage', 'purchase_date', 'is_primary')
        }),
        ('Metadata', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )