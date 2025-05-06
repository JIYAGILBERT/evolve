from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django import forms






class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):      
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('category', 'name')  # Ensures subcategory names are unique within a category
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in kilograms")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    vector = models.JSONField(blank=True, null=True)  # For storing vector embeddings
    
    def __str__(self):
        return self.name

# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)

#     def __str__(self):
#         return self.name

class Gallery(models.Model):
    feedimage = models.FileField()
    name = models.CharField(max_length=100)
    model=models.CharField(max_length=400)
    category = models.CharField(max_length=100, default='uncategorized')                                                                                                                                                                
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    # delivary = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

# class Contact(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# Create your models here.
