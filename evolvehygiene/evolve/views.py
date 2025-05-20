from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.core.exceptions import ValidationError
from .forms import ProfileForm, CategoryForm, SubCategoryForm, ContactForm
from .models import Profile, Category, SubCategory, Product, UserActivity, ContactMessage, Order, OrderItem
import random
import razorpay
from django.conf import settings

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# User views
# evolvehygiene/evolve/views.py
def home(request):
    # Get the category ID from the query parameter
    category_id = request.GET.get('category_id')
    
    # Fetch all categories by default
    categories = Category.objects.all()
    subcategories = None
    selected_category = None
    
    # If a category_id is provided, fetch its subcategories
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            subcategories = SubCategory.objects.filter(category=selected_category)
        except Category.DoesNotExist:
            # If the category doesn't exist, show all categories
            selected_category = None
            subcategories = None
    
    # Fetch featured products (not filtered by subcategory)
    products = Product.objects.all()[:8]  # Limiting to 8 featured products
    cart = request.session.get('cart', {})
    
    return render(request, 'user/home.html', {
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': selected_category,
        'products': products,
        'cart': cart,
    })
def getusername(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['email'] = user.email
            return redirect('verifyotp')
        except User.DoesNotExist:
            messages.error(request, "Username does not exist.")
            return redirect('getusername')
    return render(request, 'user/getusername.html')

def usersignup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')

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
            return redirect('user_login')
    return render(request, "user/usersignup.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Log the user activity
            UserActivity.objects.create(
                user=user,
                email=user.email,
                is_active=user.is_active
            )
            request.session['username'] = user.username
            messages.success(request, 'Login successful!')
            # Check if the user is a superuser
            if user.is_superuser:
                return redirect('admin-home')  # Redirect superuser to admin-home
            return redirect('home')  # Redirect regular user to home
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'user/user_login.html')

def passwordreset(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confpassword')
        if confirmpassword != password:
            messages.error(request, "Passwords do not match.")
        else:
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                del request.session['email']
                messages.success(request, "Your password has been reset successfully.")
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, user)
                return redirect('user_login') 
            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
                return redirect('getusername')
    return render(request, "user/password-reset.html")

@login_required
def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('home')

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'user/profile.html', {'profile': profile})

def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('Phone number should contain only digits')

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            try:
                validate_phone(phone)
                profile.phone = phone
                profile.address = address
                profile.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'user/profile_edit.html', {'form': form})

def about_us(request):
    return render(request, 'user/about_us.html')


def verifyotp(request):
    # Placeholder for OTP verification logic
    return render(request, 'user/verifyotp.html')

# User Subcategory View
def subcategory_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'user/subcategory_view.html', {
        'category': category,
        'subcategories': subcategories

    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Initialize cart in session if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    # Add product to cart or increment quantity
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_items = 0
    subtotal = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
        total_items += quantity
        subtotal += total_price

    total = subtotal  # Add shipping or other fees here if needed

    return render(request, 'user/cart.html', {
        'cart_items': cart_items,
        'total_items': total_items,
        'subtotal': subtotal,
        'total': total
    })


def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())  # Sum of quantities
    return {'cart_count': cart_count}

def buy_now(request, product_id):
    # Add the product to the cart and redirect to payment options
    product = get_object_or_404(Product, id=product_id)
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    cart[str(product_id)] = 1  # Set quantity to 1 for Buy Now
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('payment_options')

def checkout(request):
    # Redirect to payment options if cart is not empty
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty. Add some products to proceed.")
        return redirect('our_products')
    return redirect('payment_options')

def payment_options(request):
    # Display payment options (Razorpay or COD)
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty. Add some products to proceed.")
        return redirect('our_products')

    cart_items = []
    total_items = 0
    subtotal = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
        total_items += quantity
        subtotal += total_price

    total = subtotal  # Add shipping or other fees here if needed

    return render(request, 'user/payment_options.html', {
        'cart_items': cart_items,
        'total_items': total_items,
        'subtotal': subtotal,
        'total': total
    })

@login_required
def razorpay_payment(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('our_products')

        # Calculate total amount
        total_amount = 0
        cart_items = []
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price
            })
            total_amount += total_price

        # Convert total_amount to paise (Razorpay expects amount in smallest currency unit)
        amount_in_paise = int(total_amount * 100)

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount_in_paise,
            "currency": settings.CURRENCY,
            "payment_capture": "1"  # Auto-capture payment
        })

        # Create Order in database
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_method='razorpay',
            razorpay_order_id=razorpay_order['id']
        )

        # Add OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Clear the cart
        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'user/razorpay_payment.html', {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount_in_paise,
            'currency': settings.CURRENCY,
            'callback_url': request.build_absolute_uri('/order-success/' + str(order.id) + '/')
        })

    return redirect('payment_options')

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_method == 'razorpay' and order.payment_status == 'pending':
        # Verify Razorpay payment
        razorpay_payment_id = request.GET.get('razorpay_payment_id', '')
        if razorpay_payment_id:
            order.razorpay_payment_id = razorpay_payment_id
            order.payment_status = 'completed'
            order.save()
        else:
            order.payment_status = 'failed'
            order.save()
            messages.error(request, "Payment failed. Please try again.")
            return redirect('cart')

    return render(request, 'user/order_success.html', {'order': order})

# evolvehygiene/evolve/views.py
@login_required
def cash_on_delivery(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('our_products')

        # Calculate total amount
        total_amount = 0
        cart_items = []
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_price = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price
            })
            total_amount += total_price

        # Create Order in database with COD
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_method='cod',
            payment_status='pending'  # COD orders remain pending until delivery
        )

        # Add OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        # Clear the cart
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    return redirect('payment_options')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]  # Fetch related products
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'user/product_detail.html', context)



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]  # Fetch related products
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'user/product_detail.html', context)



def our_products(request):
    # Fetch all products and randomize their order
    products = list(Product.objects.all())
    random.shuffle(products)  # Randomize the list of products
    
    # Calculate discount for each product
    for product in products:
        if product.offer_price and product.offer_price != 0:  # Avoid division by zero
            product.discount = round(100 - (product.price / product.offer_price * 100))
        else:
            product.discount = 0
    
    # Get the cart from session
    cart = request.session.get('cart', {})
    
    context = {
        'products': products,
        'cart': cart
    }
    return render(request, 'user/our_products.html', context)


def add_to_wishlist(request, product_id):
    # Placeholder: Add product to wishlist (using session for now)
    product = get_object_or_404(Product, id=product_id)
    # Add to session-based wishlist
    request.session['wishlist'] = request.session.get('wishlist', {})
    request.session['wishlist'][str(product_id)] = request.session['wishlist'].get(str(product_id), 0) + 1
    request.session.modified = True
    messages.success(request, f"{product.name} added to your wishlist!")
    return redirect('our_products')


# evolve/views.py
def wishlist(request):
    wishlist = request.session.get('wishlist', {})
    products = []
    for product_id in wishlist.keys():
        product = get_object_or_404(Product, id=product_id)
        products.append({'product': product, 'quantity': wishlist[product_id]})
    return render(request, 'user/wishlist.html', {'wishlist_items': products})


def contact_us(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to send a message.")
            return redirect('user_login')
        
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact_us')
    else:
        form = ContactForm()

    return render(request, 'user/contact_us.html', {'form': form})

@login_required
def notifications(request):
    contact_messages = ContactMessage.objects.all().order_by('-is_read', '-created_at')
    return render(request, 'admin/notifications.html', {'contact_messages': contact_messages})

@login_required
def mark_notification_read(request, message_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
    
    message = get_object_or_404(ContactMessage, id=message_id)
    message.is_read = True
    message.save()
    messages.success(request, "Message marked as read.")
    return redirect('notifications')











# Admin views

# Admin Homepage
def admin_home(request):
    categories = Category.objects.all()
    return render(request, 'admin/admin-home.html', {'categories': categories})

# Category List
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        Category.objects.create(name=name, image=image)
        messages.success(request, 'Category added successfully!')
        return redirect('category_list')
    return render(request, 'admin/add_category.html')


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin-home')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/edit_category.html', {'form': form, 'category': category})


def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('admin-home')
    return render(request, 'admin/delete_category.html', {'category': category})


def admin_subcategory_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'admin/admin-subcategory.html', {
        'category': category,
        'subcategories': subcategories
    })


def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'admin/subcategory_list.html', {'subcategories': subcategories})


def add_subcategory(request, category_id=None):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            subcategory = form.save()
            messages.success(request, 'Subcategory added successfully!')
            if category_id:
                return redirect('admin_subcategory_view', category_id=category_id)
            return redirect('subcategory_list')
    else:
        initial = {'category': category_id} if category_id else {}
        form = SubCategoryForm(initial=initial)
    return render(request, 'admin/add_subcategory.html', {'form': form})


def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategory updated successfully!')
            return redirect('admin_subcategory_view', category_id=subcategory.category.id)
    else:
        form = SubCategoryForm(instance=subcategory)
    return render(request, 'admin/edit_subcategory.html', {'form': form, 'subcategory': subcategory})


def delete_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    category_id = subcategory.category.id
    if request.method == 'POST':
        subcategory.delete()
        messages.success(request, 'Subcategory deleted successfully!')
        return redirect('admin_subcategory_view', category_id=category_id)
    return render(request, 'admin/delete_subcategory.html', {'subcategory': subcategory})



# Search
def search(request):
    query = request.GET.get('q')
    if query:
        categories = Category.objects.filter(name__icontains=query)
        subcategories = SubCategory.objects.filter(name__icontains=query)
        products = Product.objects.filter(name__icontains=query)  # Assuming Product model
    else:
        categories, subcategories, products = [], [], []
    return render(request, 'search_results.html', {
        'query': query,
        'categories': categories,
        'subcategories': subcategories,
        'products': products
    })

def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
    products = products.order_by('-created_at')
    return render(request, 'admin/product_list.html', {'products': products})



def add_product(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    # Define star rating choices for the template
    star_rating_choices = [(i, str(i)) for i in range(1, 6)]  # [(1, '1'), (2, '2'), ..., (5, '5')]
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        small_description = request.POST.get('small_description')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        is_available = request.POST.get('is_available') == 'on'
        weight_or_volume = request.POST.get('weight_or_volume')
        star_rating = request.POST.get('star_rating')

        if category_id and subcategory_id:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            if subcategory.category.id != int(category_id):
                messages.error(request, 'Selected subcategory does not belong to the chosen category.')
                return render(request, 'admin/add_product.html', {
                    'categories': categories,
                    'subcategories': subcategories,
                    'star_rating_choices': star_rating_choices
                })

        product = Product(
            name=name,
            description=description,
            small_description=small_description,
            brand=brand,
            price=price,
            offer_price=offer_price if offer_price else None,
            stock=stock,
            image=image,
            is_available=is_available,
            weight_or_volume=weight_or_volume,
            star_rating=star_rating
        )

        if category_id:
            product.category = Category.objects.get(id=category_id)
        if subcategory_id:
            product.subcategory = SubCategory.objects.get(id=subcategory_id)

        product.save()
        messages.success(request, 'Product added successfully!')
        return redirect('product_list')

    return render(request, 'admin/add_product.html', {
        'categories': categories,
        'subcategories': subcategories,
        'star_rating_choices': star_rating_choices
    })


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    star_rating_choices = [(i, str(i)) for i in range(1, 6)]  # [(1, '1'), (2, '2'), ..., (5, '5')]
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.small_description = request.POST.get('small_description')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        product.brand = request.POST.get('brand')
        product.price = request.POST.get('price')
        product.offer_price = request.POST.get('offer_price') or None
        product.stock = request.POST.get('stock')
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        product.is_available = request.POST.get('is_available') == 'on'
        product.weight_or_volume = request.POST.get('weight_or_volume')
        product.star_rating = request.POST.get('star_rating')

        if category_id and subcategory_id:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            if subcategory.category.id != int(category_id):
                messages.error(request, 'Selected subcategory does not belong to the chosen category.')
                return render(request, 'admin/edit_product.html', {
                    'product': product,
                    'categories': categories,
                    'subcategories': subcategories,
                    'star_rating_choices': star_rating_choices
                })

        if category_id:
            product.category = Category.objects.get(id=category_id)
        else:
            product.category = None
        if subcategory_id:
            product.subcategory = SubCategory.objects.get(id=subcategory_id)
        else:
            product.subcategory = None

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')

    return render(request, 'admin/edit_product.html', {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
        'star_rating_choices': star_rating_choices
    })

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')

# AJAX view to fetch subcategories based on selected category
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def notifications(request):
    activities = UserActivity.objects.all().order_by('-login_date')
    return render(request, 'admin/notifications.html', {'activities': activities})

