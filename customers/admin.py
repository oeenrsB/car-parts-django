from django.contrib import admin
from .models import Customer, Address, CustomerVehicle

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'membership']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'is_default']

@admin.register(CustomerVehicle)
class CustomerVehicleAdmin(admin.ModelAdmin):
    list_display = ['customer', 'vehicle', 'nickname', 'is_primary']