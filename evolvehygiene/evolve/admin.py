from .models import ContactMessage, Gallery
from .models import Category, SubCategory, Product
from django.contrib import admin
# from .models import Gallery


admin.site.register(Gallery)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')




class SubCategoryInline(admin.TabularInline):  # or admin.StackedInline
    model = SubCategory
    extra = 1  # Number of empty forms to display

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [SubCategoryInline]  # Show subcategories when editing category

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'offer_price', 'subcategory', 'rating')
    list_filter = ('subcategory__category', 'subcategory')
    search_fields = ('name', 'details')
    readonly_fields = ('rating',)  # If rating is calculated automatically
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'details', 'subcategory')
        }),
        ('Pricing', {
            'fields': ('price', 'offer_price')
        }),
        ('Other Details', {
            'fields': ('weight', 'rating', 'vector')
        }),
    )