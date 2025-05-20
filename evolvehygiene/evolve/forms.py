# evolve/forms.py
from django import forms
from .models import Profile, Category, SubCategory

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'image']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email")
    subject = forms.CharField(max_length=200, required=True, label="Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")