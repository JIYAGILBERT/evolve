from .models import ContactMessage, Gallery
from django.contrib import admin
# from .models import Gallery


admin.site.register(Gallery)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')