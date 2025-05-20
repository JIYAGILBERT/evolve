# evolve/admin.py
from django.contrib import admin
from .models import Profile, Category, SubCategory, Product, UserActivity

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'brand', 'price', 'offer_price', 'stock', 'is_available', 'star_rating')
    list_filter = ('category', 'subcategory', 'is_available')
    search_fields = ('name', 'brand', 'description', 'small_description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'small_description', 'category', 'subcategory', 'brand')
        }),
        ('Pricing and Stock', {
            'fields': ('price', 'offer_price', 'stock', 'is_available')
        }),
        ('Additional Info', {
            'fields': ('image', 'weight_or_volume', 'star_rating')
        }),
    )

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'login_date', 'is_active')
    list_filter = ('is_active', 'login_date')
    search_fields = ('user__username', 'email')
    ordering = ('-login_date',)