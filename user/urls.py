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
    path('auction_detail/products', views.products, name='products'),
    path('add-to-cart', views.addCart, name ='add-to-cart'),
    path('product_detail/home', views.homee, name= 'homee'),
    path('checkout', views.checkout, name ='checkout'),
    path('placeorder', views.placeorder, name='placeorder'),
    path('product_detail/checkout',views.checkout, name = 'checkout'),
    path('product_detail/makeoffer', views.makeoffer, name='makeoffer'),

    path('remove/<int:product_id>', views.remove, name='remove'),
    path('update_quantity', views.update, name='update_quantity'),
    path('rating', views.rating, name = 'rating'),
    path('logout_view', views.logout_view, name='logout_view'),

    path('update_address',views.updateadd, name='update_address'),
    path('cancelorder',views.cancelorder, name='cancelorder'),
    path('canceloffer',views.canceloffer, name='canceloffer'),
    
    #index page template urls
    path('info', views.info, name = 'aboutt'),
    path('auctions', views.auctions, name = 'auctionn'),
    path('product', views.product, name = 'productss'),
    
]
