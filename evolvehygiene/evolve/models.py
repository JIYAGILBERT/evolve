from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    feedimage = models.ImageField(upload_to='gallery_images/')
    name = models.CharField(max_length=100)
    model=models.CharField(max_length=400)
    offers=models.CharField(max_length=400)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    # delivary = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Create your models here.
