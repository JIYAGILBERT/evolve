from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from.models import *

from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')

def about_us(request):
    return render(request, 'about_us.html')
    
def our_product(request):
    return render(request, 'our_product.html')


def contact(request):
    return render(request, 'contact.html')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages

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

# super user check
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect superusers

            return redirect('user_home')  # Redirect normal users
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('landing_page.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


def user_home(request):
    return render(request, 'user_home.html')
