# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login,logout
# from django.core.mail import send_mail
# from django.conf import settings
# import random
# from datetime import datetime, timedelta
# from django.contrib.auth.models import User
# from django.contrib import messages
# from.models import *
# from . import views
# from django.contrib.auth import authenticate, login as auth_login
# from django.shortcuts import render, redirect
# from django.contrib import messages




# from django.shortcuts import render

# def product_upload(request):
#     if request.method == 'POST' and 'image' in request.FILES:  
#         myimage = request.FILES['image']  
#         name=request.POST.get("todo")
#         price=request.POST.get("date")
#         # todo311=request.POST.get("course")
#         quanty=request.POST.get("quant")
#         mod=request.POST.get("model")
#         off=request.POST.get("offers")
#         obj=Gallery(name=name,price=price,model=mod,quantity=quanty,offers=off,feedimage=myimage,user=request.user)
#         obj.save()
#         data=Gallery.objects.all()
#         return redirect(admin_dashboard)
#     gallery_images = Gallery.objects.all()
#     return render(request, "product_upload.html")

# def landing_page(request):
#     return render(request, 'landing_page.html')

# def about_us(request):
#     return render(request, 'about_us.html')
    
# def our_product(request):
#     return render(request, 'our_product.html')


# def contact(request):
#     return render(request, 'contact.html')

# def register(request):
#     if request.POST:
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         confirmpassword = request.POST.get('Confirmpassword')
#         print(email,username,password,confirmpassword)
#         # Validate form fields
#         if not username or not email or not password or not confirmpassword:
#             messages.error(request, 'All fields are required.')
#         elif confirmpassword != password:
#             messages.error(request, "Passwords do not match.")
#         elif User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists.")
#         elif User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#         else:
#             # Create the user
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.save()
#             messages.success(request, "Account created successfully!")
#             return redirect('login')  # Redirect to login page

#     return render(request,"register.html")


# def login(request):
#     if 'username' in request.session:
#         return redirect('user_home')  

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             auth_login(request, user)
#             request.session['username'] = username

# # super user check
#             if user.is_superuser:
#                 return redirect('admin_dashboard')  # Redirect superusers

#             return redirect('user_home')  # Redirect normal users
#         else:
#             messages.error(request, "Invalid credentials.")

#     return render(request, 'login.html')

# def logoutuser(request):
#     logout(request)
#     request.session.flush()
#     return redirect('landing_page')

# def admin_dashboard(request):
#     data = Gallery.objects.all()
#     gallery_images = Gallery.objects.filter(user=request.user)
#     return render(request,'admin_dashboard.html',{"gallery_images": gallery_images})
# def user_home(request):
#     return render(request, 'user_home.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .models import Gallery
from django.core.exceptions import ValidationError

# def product_upload(request):
#     if request.method == 'POST' and 'image' in request.FILES:  
#         myimage = request.FILES['image']  # Get the uploaded image file
#         name = request.POST.get("todo")
#         price = request.POST.get("date")
#         quantity = request.POST.get("quant")
#         model = request.POST.get("model")
#         off = request.POST.get("offers")
        
#         # Check if all fields are provided
#         if not name or not price or not quantity or not model:
#             messages.error(request, 'All fields must be filled out.')
#             return redirect('product_upload')  # Ensure the user gets a message if validation fails

#         # Create a new Gallery object and save it
#         try:
#             obj = Gallery(name=name, price=price, model=model, quantity=quantity, offers=off, feedimage=myimage, user=request.user)
#             obj.save()
#             messages.success(request, 'Product uploaded successfully.')
#             return redirect('admin_dashboard')  # Redirect to the admin dashboard after saving
#         except ValidationError as e:
#             messages.error(request, f"Error: {str(e)}")
#             return redirect('product_upload')
#     else:
#         gallery_images = Gallery.objects.all()  # Get all images to show on the page
#         return render(request, "product_upload.html", {"gallery_images": gallery_images})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Gallery  # Make sure you have this model imported

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Gallery
from decimal import Decimal

def product_upload(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Get the uploaded image and other form data
        myimage = request.FILES['image']
        name = request.POST.get("todo")
        price = request.POST.get("date")
        quantity = request.POST.get("quant")
        model = request.POST.get("model")
        offers = request.POST.get("offers")  # Offers field is optional

        # Validate if required fields are provided
        if not name or not price or not quantity or not model:
            messages.error(request, 'All required fields (Company, Price, Quantity, Model) must be filled out.')
            return redirect('product_upload')  # Redirect back to the form with error message
        
        # Validate price and quantity (make sure they are valid decimals)
        try:
            price = Decimal(price)
            quantity = Decimal(quantity)
        except (ValueError, InvalidOperation):
            messages.error(request, 'Price and Quantity must be valid numbers.')
            return redirect('product_upload')

        # Create and save a new Gallery object
        try:
            obj = Gallery(
                name=name, 
                price=price, 
                model=model, 
                quantity=quantity, 
                offers=offers, 
                feedimage=myimage, 
                user=request.user
            )
            obj.save()
            messages.success(request, 'Product uploaded successfully.')
            return redirect('admin_dashboard')  # Redirect to admin dashboard after saving
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('product_upload')  # Redirect back to the form with error message

    else:
        gallery_images = Gallery.objects.all()  # Get all gallery images
        return render(request, "product_upload.html", {"gallery_images": gallery_images})

def landing_page(request):
    return render(request, 'landing_page.html')

def about_us(request):
    return render(request, 'about_us.html')

def our_product(request):
    return render(request, 'our_product.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('Confirmpassword')

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
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to login page

    return render(request, "register.html")

def login(request):
    if 'username' in request.session:
        return redirect('user_home')  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            request.session['username'] = username

            # Super user check
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect superusers

            return redirect('user_home')  # Redirect normal users
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('landing_page')

def admin_dashboard(request):
    data = Gallery.objects.all()
    gallery_images = Gallery.objects.filter(user=request.user)
    return render(request, 'admin_dashboard.html', {"gallery_images": gallery_images})

def user_home(request):
    return render(request, 'user_home.html')


def contact_us(request):
    return render(request, 'contact_us.html')
