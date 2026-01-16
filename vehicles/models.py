from django.db import models

class Make(models.Model):
    """Car manufacturers"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Model(models.Model):
    """Car models"""
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    class Meta:
        ordering = ['name']
        unique_together = ['make', 'name']
    
    def __str__(self):
        return f"{self.make.name} {self.name}"


class Vehicle(models.Model):
    """Specific vehicle year/trim"""
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='vehicles')
    year = models.IntegerField()
    trim = models.CharField(max_length=100, blank=True)
    engine = models.CharField(max_length=100, blank=True)
    body_type = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-year', 'trim']
        unique_together = ['model', 'year', 'trim']
    
    def __str__(self):
        trim_text = f" {self.trim}" if self.trim else ""
        return f"{self.year} {self.model.make.name} {self.model.name}{trim_text}"