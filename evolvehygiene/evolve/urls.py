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
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)