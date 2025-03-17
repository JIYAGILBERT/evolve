from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
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
    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('Confirmpassword')
        print(email,username,password,confirmpassword)
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
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password,user=request.user)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to login page

    return render(request,"register.html")



def userlogin(request):
    if 'username' in request.session:
        return redirect('user_home')   

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username

            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('landing_page')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'userlogin.html')


def user_home(request):
    return render(request, 'user_home.html')


def about_us(request):
    return render(request, 'about_us.html')



def our_product(request):
    return render(request, 'our_product.html')


@login_required(login_url='/accounts/login/')  # Redirect to login if not logged in
def contact_us(request):
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


def thank_you_page(request):
    return render(request, 'thank_you_page.html')


    
def product_upload(request):
    if request.method == 'POST':
        # Fetch form data properly
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        model = request.POST.get("model")
        offers = request.POST.get("offers")
        myimage = request.FILES['image']  # Correct way to handle files!

        # Ensure no fields are missing (optional: add error handling)
        if not name:
            return render(request, "product_upload.html", {"error": "Name is required"})

        # Save to the database
        obj = Gallery.objects.create(
            name=name,
            price=price,
            model=model,
            quantity=quantity,
            offers=offers,
            feedimage=myimage
        )
        obj.save()

        return redirect(admin_dashboard)

    gallery_images = Gallery.objects.all()
    return render(request, "product_upload.html", {"gallery_images": gallery_images})



def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('landing_page')

def admin_dashboard(request):
    gallery_items = Gallery.objects.all()

    for item in gallery_items:
        if not item.feedimage:  # Safely handle missing images
            item.feedimage_url = None
        else:
            item.feedimage_url = item.feedimage.url

    return render(request, "admin_dashboard.html", {"gallery_items": gallery_items})


def delete_g(request,id):
    feeds=Gallery.objects.filter(pk=id)
    feeds.delete()
    return redirect('product_upload')


# @login_required
def edit_g(request, id):
    gallery_image = get_object_or_404(Gallery, pk=id, user=request.user)
    
    if request.method == 'POST':
        myimage = request.FILES['image']  
        name=request.POST.get("todo")
        price=request.POST.get("date")
        # todo311=request.POST.get("course")
        quanty=request.POST.get("quant")
        mod=request.POST.get("model") 
        off=request.POST.get("offers")
        
        if not name or not price or not quanty or not mod or not off:
            messages.error(request, "All fields are required.")
            return render(request, 'upload_product.html', {'data1': gallery_image})
        
        
        gallery_image.name = name
        gallery_image.price = price
        gallery_image.quantity = quanty
        gallery_image.model = mod
        gallery_image.offers = off
        if myimage: 
            gallery_image.feedimage = myimage
        gallery_image.save()

        messages.success(request, "Gallery item updated successfully!")
        return redirect('admin_dashboard')







