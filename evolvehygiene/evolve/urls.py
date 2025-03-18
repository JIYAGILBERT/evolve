from django.contrib import admin
from evolve import views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.landing_page, name='landing_page'),
    path('about_us',views.about_us, name='about_us'),   
    path('our_product',views.our_product, name='our_product'),   
    # path('contact',views.contact, name='contact'), 
    path('userlogin',views.userlogin, name='userlogin'), 
    path('user_home',views.user_home, name='user_home'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('register',views.register, name='register'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('product_upload',views.product_upload, name='product_upload'),
    path('contact_us',views.contact_us, name='contact_us'),
    path('thank_you_page',views.thank_you_page, name='thank_you_page'),
     path('accounts/', include('django.contrib.auth.urls')),  # <-- Add this line!
     
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
