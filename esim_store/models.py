from django.db import models
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)  # ISO country code
    flag_image = models.ImageField(upload_to='flags/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return self.name

class ESIMPlan(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    data_amount = models.CharField(max_length=50)  # e.g., "1GB", "5GB", "10GB"
    validity_days = models.IntegerField()  # e.g., 7, 30, 90
    countries = models.ManyToManyField(Country, related_name='esim_plans')
    image = models.ImageField(upload_to='plans/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class PageContent(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Page Contents"
    
    def __str__(self):
        return self.title

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    esim_plan = models.ForeignKey(ESIMPlan, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    def __str__(self):
        return f"Order {self.id} - {self.name}"