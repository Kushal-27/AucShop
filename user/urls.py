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
    path('auction_detail/<int:product_id>', views.auction_detail, name = 'auction_detail'),
    path('place_bid/<int:auction_id>', views.place_bid, name = 'place_bid'),
    path('add-to-cart', views.addCart, name ='add-to-cart'),
    path('product_detail/home', views.homee, name= 'homee'),
    
    #index page template urls
    path('info', views.info, name = 'aboutt'),
    path('auctions', views.auctions, name = 'auctionn'),
    path('product', views.product, name = 'productss'),
    
]
