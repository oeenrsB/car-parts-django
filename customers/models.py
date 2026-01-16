from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    MEMBERSHIP_CHOICES = [
        ('R', 'Regular'),
        ('S', 'Silver'),
        ('G', 'Gold'),
        ('P', 'Platinum'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default='R')
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f"{self.street}, {self.city}"


class CustomerVehicle(models.Model):
    """Customer's garage - saved vehicles"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    vin = models.CharField(max_length=17, blank=True)
    mileage = models.IntegerField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['customer', 'vehicle']
    
    def __str__(self):
        nickname_text = f" ({self.nickname})" if self.nickname else ""
        return f"{self.customer.user.username}'s {self.vehicle}{nickname_text}"