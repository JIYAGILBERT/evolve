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
                return redirect('user/admin_dashboard')
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
    return redirect('user/userlogin')

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
    if request.method == 'POST':
        # Fetch form data properly
        name = request.POST.get("name")
        price = request.POST.get("price")
        # quantity = request.POST.get("quantity")
        model = request.POST.get("model")
        myimage = request.FILES.get('image')  # Safer way to get the file

        # Optional: Basic error handling
        if not name or not price or not model or not myimage:
            return render(request, "/admin/product_upload.html", {"error": "All fields are required!"})

        # Save to the database
        obj = Gallery.objects.create(
            name=name,
            price=price,
            model=model,
            # quantity=quantity,
            feedimage=myimage
        )
        obj.save()

        return redirect('admin/admin_dashboard')

    # Fetch images for display
    gallery_images = Gallery.objects.all()
    return render(request, "admin/product_upload.html", {"gallery_images": gallery_images})


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





