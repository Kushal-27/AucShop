from django.contrib import admin
from .models import Vendor, Product, Auction, Rating, Cart, Offer, Order, Bid

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(Offer)
admin.site.register(Order)
admin.site.register(Bid)
admin.site.register(Auction)