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






def landing_page(request):
    return render(request, 'landing_page.html')




def register(request):
    if request.method == 'POST':  # Check if the request method is POST
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('Confirmpassword')
        print(email, username, password, confirmpassword)

        # Validate form fields
        if not username or not email or not password or not confirmpassword:
            messages.error(request, 'All fields are required.')
        elif confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            # Create the user without passing 'user=request.user'
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('userlogin')  # Redirect to login page

    return render(request, "register.html")



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def userlogin(request):
    # If user already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('user_home')

    # Handle login form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Start session automatically
            # Redirect based on user type
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('user_home')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'userlogin.html')


def logoutuser(request):
    logout(request)
    # request.session.flush()
    return redirect('userlogin')

def user_home(request):
    return render(request, 'user_home.html')


def about_us(request):
    return render(request, 'about_us.html')



def our_product(request):
    # Fetch all products from the Gallery model
    gallery_items = Gallery.objects.all()

    # Ensure the items are passed to the template properly
    return render(request, "our_product.html", {"gallery_items": gallery_items})


# @login_required(login_url='userlogin')  # Redirect to login if not logged in
def contact_us(request):
    if 'username' in request.session:
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
                return redirect('thank_you_page')  # Redirect to 'thank you' page

        else:
            form = ContactForm()

        return render(request, 'contact_us.html', {'form': form})
    else:
        return redirect('userlogin')    


def thank_you_page(request):
    return render(request, 'thank_you_page.html')


    
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
            return render(request, "product_upload.html", {"error": "All fields are required!"})

        # Save to the database
        obj = Gallery.objects.create(
            name=name,
            price=price,
            model=model,
            # quantity=quantity,
            feedimage=myimage
        )
        obj.save()

        return redirect('admin_dashboard')

    # Fetch images for display
    gallery_images = Gallery.objects.all()
    return render(request, "product_upload.html", {"gallery_images": gallery_images})


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
    return render(request, "admin_dashboard.html", {"gallery_items": gallery_items})



def delete_g(request,id):
    feeds=Gallery.objects.filter(pk=id)
    feeds.delete()
    return redirect('admin_dashboard')


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
        return redirect("admin_dashboard")

    return render(request, "product_upload.html", {"data1": product})

def search_result(request):
    query = request.GET.get('q')
    results = Gallery.objects.filter(name__icontains=query) if query else None
    return render(request, 'search_results.html', {'results': results, 'query': query}) 







