from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from .models import Gallery
from.models import *
from . import views
import random
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Category



def landing_page(request):
    # if not request.user.is_authenticated:
    #     return redirect('user/userlogin')
    return render(request, "landing_page.html")



def userlogin(request):
    if request.user.is_authenticated:
        return redirect('landing_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill in both fields.")
            return redirect('user/userlogin')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ This ensures the user is logged in
            request.session['username'] = username  # ✅ Store username in session
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('landing_page')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'user/userlogin.html')





def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('Confirmpassword')

        # Validation
        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('user/userlogin')

    return render(request, "register.html")


def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('userlogin')

def user_home(request):
    return render(request, 'user/user_home.html')


def about_us(request):
    return render(request, 'user/about_us.html')



def our_product(request):
    # Fetch all products from the Gallery model
    gallery_items = Gallery.objects.all()

    # Ensure the items are passed to the template properly
    return render(request, "user/our_product.html", {"gallery_items": gallery_items})


# @login_required(login_url='userlogin')  # Redirect to login if not logged in
def contact_us(request):
    if request.session.get('username'):  # ✅ Ensure session exists
        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                contact_message = form.save()

                # Send email
                send_mail(
                    subject=f"New Contact Form Submission: {contact_message.subject}",
                    message=f"Name: {contact_message.name}\nEmail: {contact_message.email}\n\nMessage:\n{contact_message.message}",
                    from_email="your_email@example.com",
                    recipient_list=["jiyagilbert1@gmail.com"],
                    fail_silently=False,
                )
                return redirect('thank_you_page')

        else:
            form = ContactForm()

        return render(request, 'user/contact_us.html', {'form': form})  # ✅ Pass form to template

    else:
        return redirect('user/userlogin')



def thank_you_page(request):
    return render(request, 'user/thank_you_page.html')


    
def product_upload(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        weight = request.POST.get('weight')
        details = request.POST.get('details')
        rating = request.POST.get('rating')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')

        # Validation (you can add more)
        if not all([name, image, price, weight, details, category_id, subcategory_id]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'admin/product_upload.html', {'categories': categories})

        try:
            category = Category.objects.get(id=category_id)
            subcategory = SubCategory.objects.get(id=subcategory_id)

            product = Product.objects.create(
                name=name,
                image=image,
                price=price,
                offer_price=offer_price if offer_price else None,
                weight=weight,
                details=details,
                rating=rating if rating else None,
                category=category,
                subcategory=subcategory,
            )
            messages.success(request, "Product uploaded successfully.")
            return redirect('product_upload')  # or redirect to a product list page
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'product_upload.html', {'categories': categories})

    return render(request, 'admin/product_upload.html', {'categories': categories})


def admin_dashboard(request):
    # Fetch products from Gallery model
    gallery_items = Gallery.objects.all()

    # Ensure every item has a valid image URL
    for item in gallery_items:
        if not item.feedimage:
            item.feedimage_url = None
        else:
            item.feedimage_url = item.feedimage.url

    # Pass gallery items to the template
    return render(request, "admin/admin_dashboard.html", {"gallery_items": gallery_items})



def delete_g(request,id):
    feeds=Gallery.objects.filter(pk=id)
    feeds.delete()
    return redirect('admin/admin_dashboard')


# @login_required
def edit_g(request, id):
    # Fetch the product or return 404 if not found
    product = get_object_or_404(Gallery, id=id)

    if request.method == "POST":
        product.name = request.POST.get("todo", product.name)
        product.price = request.POST.get("date", product.price)
       
        # Handle image update if a new one is uploaded
        if "image" in request.FILES:
            product.feedimage = request.FILES["image"]

        # Save the updated product
        product.save()
        return redirect("admin/admin_dashboard")

    return render(request, "admin/product_upload.html", {"data1": product})

def search_result(request):
    query = request.GET.get('q')
    results = Gallery.objects.filter(name__icontains=query) if query else None
    return render(request, 'user/search_results.html', {'results': results, 'query': query}) 


# def samp(request):
#     return render(request, 'contact_us.html')  
def admin_users(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        # Redirect non-admin users or unauthenticated users
        return redirect('user/loginuser')  
    users = User.objects.all()  # Fetch all users
    return render(request, 'admin/admin_users.html', {'users':users})  


def dispenser(request):
    return render(request, 'user/dispenser.html')


def cleaning_products(request):
    return render(request, 'user/cleaning_products.html')


def cleaning_products(request):
    return render(request, 'user/cleaning_products.html')




def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Category.objects.filter(name=name).exists():
            return render(request, 'admin/create_category.html', {
                'error': 'Category with this name already exists.'
            })
        try:
            Category.objects.create(name=name)
            return redirect('category_list')
        except IntegrityError:
            return render(request, 'create_category.html', {
                'error': 'An error occurred while creating the category.'
            })
    return render(request, 'admin/create_category.html')

def create_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        category = Category.objects.get(id=category_id)
        SubCategory.objects.create(category=category, name=name)
        return redirect('subcategory_list')
    
    categories = Category.objects.all()
    return render(request, 'create_subcategory.html', {'categories': categories})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})







def create_subcategory(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')

        if not name or not category_id:
            messages.error(request, "Both fields are required.")
        else:
            category = Category.objects.get(id=category_id)
            # Check if subcategory already exists
            if SubCategory.objects.filter(name=name, category=category).exists():
                messages.error(request, "This subcategory already exists for the selected category.")
            else:
                SubCategory.objects.create(name=name, category=category)
                messages.success(request, "Subcategory created successfully.")
                return redirect('create_subcategory')

    return render(request, 'admin/create_subcategory.html', {'categories': categories})





def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})

