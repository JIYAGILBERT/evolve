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
    #     return redirect('userlogin')
    return render(request, "landing_page.html")


from django.contrib.auth import authenticate, login
from django.contrib import messages

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('landing_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please fill in both fields.")
            return redirect('userlogin')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ This ensures the user is logged in
            request.session['username'] = username  # ✅ Store username in session
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('landing_page')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'userlogin.html')





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
            return redirect('userlogin')

    return render(request, "register.html")


def logoutuser(request):
    logout(request)
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

        return render(request, 'contact_us.html', {'form': form})  # ✅ Pass form to template

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


# def samp(request):
#     return render(request, 'contact_us.html')  
def admin_users(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        # Redirect non-admin users or unauthenticated users
        return redirect('loginuser')  
    users = User.objects.all()  # Fetch all users
    return render(request, 'admin_users.html', {'users':users})  


@login_required(login_url='userlogin')
def add_to_cart(request, id):
    if 'username' in request.session:
        try:
            product = Gallery.objects.get(id=id)
        except Gallery.DoesNotExist:
        
            return redirect('product_not_found')  
    
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
        
        )
        if not created:
            if cart_item.product.quantity > cart_item.quantity:
                cart_item.quantity += 1
            else:
                messages.error(request, "out of stock.")
                return redirect('cart_view')
        else:
            cart_item.quantity = 1
            cart_item.save()
            return redirect('cart_view')


@login_required
def increment_cart(request, id):
    cart_item = get_object_or_404(Cart, pk=id, user=request.user)
    if cart_item.product.quantity > cart_item.quantity:
        cart_item.quantity += 1
        cart_item.save()
    else:
        messages.error(request, "Not enough stock available.")

    return redirect('cart_view')

@login_required
def decrement_cart(request, id):
    cart_item = get_object_or_404(Cart, pk=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_view')


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_item_count = cart_items.count()
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart_item_count': cart_item_count})

@login_required
def delete_cart(request, id):
    cart_item = get_object_or_404(Cart, pk=id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')





