from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """Product categories with hierarchy"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                                null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='categories/', blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Parts manufacturers/brands"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    # logo = models.ImageField(upload_to='manufacturers/', blank=True)
    # website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('OEM', 'OEM Original'),
        ('AFT', 'Aftermarket'),
        ('PER', 'Performance'),
        ('UNI', 'Universal'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    # Pricing & Inventory
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    inventory = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10)
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='products')
    
    # Part Details
    part_number = models.CharField(max_length=100, blank=True)
    oem_part_number = models.CharField(max_length=100, blank=True)
    product_type = models.CharField(max_length=3, choices=PRODUCT_TYPE_CHOICES, default='AFT')
    is_universal = models.BooleanField(default=False)
    
    # # Physical Properties
    # weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Warranty & Support
    warranty_months = models.IntegerField(default=12)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# class ProductImage(models.Model):
#     """Multiple images per product"""
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='products/')
#     alt_text = models.CharField(max_length=255, blank=True)
#     is_primary = models.BooleanField(default=False)
#     sort_order = models.IntegerField(default=0)
    
#     class Meta:
#         ordering = ['sort_order', 'id']
# 
#     def __str__(self):
#         return f"{self.product.title} - Image {self.id}"


class ProductSpecification(models.Model):
    """Technical specifications"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        unit_text = f" {self.unit}" if self.unit else ""
        return f"{self.name}: {self.value}{unit_text}"


class ProductFitment(models.Model):
    """Which vehicles this product fits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fitments')
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, 
                                related_name='compatible_products')
    fitment_notes = models.TextField(blank=True)
    position = models.CharField(max_length=50, blank=True)
    
    class Meta:
        unique_together = ['product', 'vehicle']
    
    def __str__(self):
        return f"{self.product.title} fits {self.vehicle}"


class ProductDocument(models.Model):
    """Installation guides, manuals, etc."""
    DOCUMENT_TYPES = [
        ('INSTALL', 'Installation Guide'),
        ('MANUAL', 'User Manual'),
        ('WARRANTY', 'Warranty Info'),
        ('DIAGRAM', 'Diagram'),
        ('VIDEO', 'Video Tutorial'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    # file = models.FileField(upload_to='documents/', blank=True)
    # url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.product.title} - {self.title}"