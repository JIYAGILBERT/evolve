# evolvehygiene/evolve/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('getusername/', views.getusername, name='getusername'),
    path('verifyotp/', views.verifyotp, name='verifyotp'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('user_login/', views.user_login, name='user_login'),
    path('forgotpassword/', views.passwordreset, name='forgotpassword'),
    path('logout/', views.logoutuser, name='logout'),


    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    
    path('subcategory/<int:category_id>/', views.subcategory_view, name='subcategory_view'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('increase-quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),


    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_options/', views.payment_options, name='payment_options'),    
    path('cash_on_delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),

    path('delivery_details/<int:product_id>/', views.delivery_details, name='delivery_details'),
    path('save_delivery_details/<int:product_id>/', views.save_delivery_details, name='save_delivery_details'),
    path('order_summary/<int:product_id>/', views.order_summary, name='order_summary'),
    path('razorpay_payment/', views.razorpay_payment, name='razorpay_payment'),
   path('order_success/<int:order_id>/', views.order_success, name='order_success'),

   path('cod_captcha/', views.cod_captcha, name='cod_captcha'),
    path('track_order/<int:order_id>/', views.track_order, name='track_order'),  
    path('my_orders/', views.my_orders, name='my_orders'), 
    path('edit_delivery_details/', views.edit_delivery_details, name='edit_delivery_details'),  
    path('our_products/', views.our_products, name='our_products'),
    
    # Admin URLs
    path('admin-home/', views.admin_home, name='admin-home'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('subcategories/edit/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('admin-subcategory/<int:category_id>/', views.admin_subcategory_view, name='admin_subcategory_view'),
    path('search/', views.search, name='search'),
    
    # Product URLs
    path('product-list/', views.product_list, name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('notifications/', views.notifications, name='notifications'),
    path('mark-notification-read/<int:message_id>/', views.mark_notification_read, name='mark_notification_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)