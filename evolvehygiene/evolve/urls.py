from django.contrib import admin
from evolve import views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.landing_page, name='landing_page'),
    path('about_us',views.about_us, name='about_us'),   
    path('our_product',views.our_product, name='our_product'),   
    path('contact',views.contact, name='contact'), 
    path('login',views.login, name='login'), 
    path('user_home',views.user_home, name='user_home'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('register',views.register, name='register'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('product_upload',views.product_upload, name='product_upload'),
    path('contact_us',views.contact_us, name='contact_us'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
