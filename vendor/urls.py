from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'vendor' 
urlpatterns = [
    
    path('vendorlogin/', views.login, name ='vendorlogin'),
    path('vendorsignup/', views.register, name='vendorsignup'),
    path('vendorhome/', views.vendorhome, name='vendorhome'),
    path('vendor_profile/', views.profile, name = 'vendor_profile'),
    path('offer/', views.offer, name = 'offer'),
    path('acceptoffer/', views.acceptoffer, name = 'acceptoffer'),
    path('declineoffer/', views.declineoffer, name = 'declineoffer'),
    path('listproduct/', views.listproduct, name = 'listproduct'),
    path('createauction/', views.createauction, name = 'createauction'),
    path('logoutt/', views.logoutt, name = 'logoutt'),
]
