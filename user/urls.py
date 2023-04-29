from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name='index' ),
    path('login', views.login, name = 'login'),
    path('signup', views.signup, name = 'signup'),
    path('home', views.home, name = 'home'),
    path('about', views.about, name = 'about'),
    path('auction', views.auction, name = 'auction'),
    path('account', views.account, name = 'account'),
    path('cart', views.cart, name = 'cart'),
    path('products', views.products, name = 'products'),
    path('product_detail/<int:product_id>', views.product_detail, name = 'product_detail'),
    #index page template urls
    path('info', views.info, name = 'aboutt'),
    path('auctions', views.auctions, name = 'auctionn'),
    path('product', views.product, name = 'productss'),

]
