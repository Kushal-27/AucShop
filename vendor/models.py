from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User
# Create your models here.

class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor')
    shopname = models.CharField(max_length=255)
    pan_number = models.IntegerField(default=False)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_picture = models.ImageField(upload_to='Product_pictures/', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=100)
    quantity=  models.IntegerField(default=0)
    offers = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Auction(models.Model):
    item = models.CharField(max_length=255)
    description = models.TextField()
    seller = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='auctions_selling')
    product_picture = models.ImageField(upload_to='Product_pictures/', null=True, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_increment = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='auctions_winning', null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    status_choices = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='open')

    def __str__(self):
        return self.item
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.amount} on {self.auction.item}"
    
class Offer(models.Model):
    sender = models.ForeignKey(User, related_name='sent_offers', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='received_offers', on_delete=models.CASCADE)
    message = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    # Status of the offer, can be 'PENDING', 'ACCEPTED', or 'DECLINED'
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    address = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.vendor} - {self.product} - {self.customer}'
