from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from vendor.models import Product, Auction, Bid
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponse
User = get_user_model()
from django.db.models.functions import Random
from vendor.models import Cart, Order, Vendor, Offer, Rating
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
import pytz
from django.db.models import Max
# Create your views here.
def index(request):
    product = Product.objects.order_by(Random())[:6]
    
    rat = 0
    score = 0
    for items in product:
        ratings = Rating.objects.filter(product_id = items.id)
        if ratings:
            for rating in ratings:
                rat = rat + rating.stars
            score = rat/len(ratings)
            items.description=score
        else:
            items.description = 0
            

    return render(request, 'index.html', {'products':product})

def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username = email, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Logged in Successfully')
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')


    else:
        
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        full_name = request.POST['name']
        name_list = full_name.split()
        length = len(name_list)
        first_name = str(name_list[0])
        last_name = str(name_list[length-1])
        print(last_name)
        phone_number = request.POST['number']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already in use')
                return redirect('signup')
            else:
                user = User.objects.create_user(first_name=first_name,last_name= last_name, phone_number= phone_number, email=email,password=password1)
                user.save()
                messages.success(request,'Account created successfully! Please Login')
        else:
            messages.error(request,'Password not matching')
            return redirect('signup')

        return redirect('login')
    else: 
        return render(request, 'register.html')

@login_required(login_url='/login')
def home(request):
    product = Product.objects.order_by(Random())[:6]
    rat = 0
    score = 0
    for items in product:
        ratings = Rating.objects.filter(product_id = items.id)
        if ratings:
            for rating in ratings:
                rat = rat + rating.stars
            score = rat/len(ratings)
            items.description=score
        else:
            items.description = 0

    
    return render(request, 'home.html', {'products':product})
    
def homee(request):
    return redirect(home)
def about(request):
    return render(request, 'about.html')

def cart(request):
    user = request.user.id
    products=[]
    total_cost= 0
    cart = Cart.objects.filter(user_id=user)
    for items in cart:
        product = Product.objects.get(id = items.product_id)
        product.quantity = Cart.objects.get(product_id=product.id).quantity
        product.total= product.price*product.quantity
        products.append(product)
        total_cost = total_cost+product.total
    context = {'products':products, 'total_cost': total_cost}
    return render(request,'cart.html', context)

def auction(request):
    auction = Auction.objects.all()
    return render(request, 'auction.html', {'products':auction})

def account(request):
    if request.method == 'POST':
        return HttpResponse('test')
    else:
        
        order = Order.objects.filter(customer_id=request.user.id)
        offer = Offer.objects.filter(sender_id=request.user.id).exclude(status='Declined')
        for items in order:
            product = Product.objects.get(id = items.product_id)
            
            items.address = product.name
        
        for item in offer:
            product = Product.objects.get(id = item.product_id_id)
            item.message = product.name
        user = User.objects.get(id=request.user.id)
        context = { 'orders':order, 'offers':offer, 'user':user}
        return render(request, 'account.html',context)

def products(request):
    product = Product.objects.order_by(Random())[:9]
    return render(request, 'product.html', {'products':product})

#index page views
def info(request):
    return render(request, 'about.html')

def product(request):
    product = Product.objects.order_by(Random())[:6]
    return render(request, 'product.html', {'products':product})

def auctions(request):
    return render(request, 'auctionn.html')

def product_detail(request, product_id):
    obj = Product.objects.filter(id=product_id)
    return render(request, 'productpage.html', {'details':obj})
    
def auction_detail(request, product_id):
    obj = Auction.objects.get(id=product_id)
    
    tz = pytz.timezone('Asia/Kathmandu')
    obj.end_time = obj.end_time.astimezone(tz)
    highest_bid = Bid.objects.filter(auction_id=obj.id).order_by('-amount').first()
    if highest_bid:
        highest_bid_timestamp = highest_bid.timestamp
    context = {'auction':obj, 'lastbid':highest_bid_timestamp}
    return render(request, 'auctiondetail.html', context)

def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    highest_bid = Bid.objects.filter(auction_id=auction_id).order_by('-amount').first()
    if highest_bid:
        highest_bid_timestamp = highest_bid.timestamp
    
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        current_time = timezone.now()

        if bid_amount is not None and bid_amount != '' and float(bid_amount) > auction.current_bid:
            bid = Bid.objects.create(auction=auction, user=request.user, amount=float(bid_amount), timestamp=current_time)
            auction.current_bid = bid.amount
            auction.save()
            messages.success(request, 'Your bid has been placed.')
            
            return redirect('auction_detail', product_id=auction.id)
        else:
            messages.error(request, 'Your bid must be higher than the current bid.')

    context = {'auctions':auction,'lastbid':highest_bid_timestamp}
    return render(request, 'auctiondetail.html', context)

def addCart(request):
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST['product_id']
            print(product_id)
            quantity = 1
            user = request.user.id
            product_check = Product.objects.get(id=product_id)
            if(product_check):
                if product_check.quantity >= quantity:
                    if Cart.objects.filter(product_id=product_id).exists():
                        
                        cart_item = Cart.objects.get(product_id=product_id)
                        if cart_item.quantity < product_check.quantity:
                            cart_item.quantity = cart_item.quantity+1
                            cart_item.save()
                            
                            return JsonResponse({'status':'Product Added Successfully'})
                        else:
                            return JsonResponse({'status':'Not enough product quantity'})
                    else:
                        cart_item = Cart.objects.create(user_id=user, product_id=product_id,  quantity=quantity)
                        return JsonResponse({'status':'Product Added Successfully'})
                else:
                    return JsonResponse({'status':'Product out of stock'})
            else:
                return JsonResponse({'status':'No Such Product'})
            
        else:
            return JsonResponse({'status':'Login to Continue'})
    else:
        return redirect('/')
    

def checkout(request):
    if request.method == 'POST':
        total = 0
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('id')
        product = Product.objects.get(id=product_id)
        if product.quantity>=quantity:
            product.quantity = quantity
            price = product.price
            total = price * quantity
            
            context = {'products':product,'user':request.user,'total':total}
            return render(request,'checkout.html',context)
        else:
            messages.error(request,"Not enough quantity")
            return redirect(reverse('product_detail', args=[product_id]))
    else:
        
        items = []
        total = 0
        cart = Cart.objects.filter(user_id=request.user.id)
        for item in cart:
            product = Product.objects.get(id=item.product_id)
            product.quantity = item.quantity
            total = product.price*item.quantity + total
            items.append(product)
        context = {'cart':items,'user':request.user,'total':total}
        
        return render(request,'checkout.html',context)

def placeorder(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        cart = Cart.objects.filter(user_id=request.user.id)
        for item in cart:
            product = Product.objects.get(id=item.product_id)
            product.quantity = product.quantity-item.quantity
            order = Order.objects.create(quantity=item.quantity,order_status="PROCESSING",customer_id=item.user_id,product_id= item.product_id,vendor_id=product.vendor_id,address=address)
            order.save()
            product.save()
        cart.delete()
        
        messages.success(request,"Order Placed Successfully")
        return redirect('home')
    

def makeoffer(request):
    if request.method == "POST":
        offer_price = float(request.POST.get('price'))
        message = request.POST.get('message')
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('id')
        product = Product.objects.get(id=product_id)
        if product.quantity >= quantity:
            offer = Offer.objects.create(message=message,price=offer_price,sender_id=request.user.id,product_id_id=product_id)
            offer.save()
            messages.success(request,'Your offer has been sent')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request,'Not enough Quantity')
            return redirect(reverse('product_detail', args=[product_id]))


def remove(request, product_id):
    cart = Cart.objects.get(user_id=request.user.id , product_id=product_id)
    cart.delete()
    messages.success(request,"Item removed from the cart")
    return redirect(request.META.get('HTTP_REFERER'))

def update(request):
    quantity = int(request.POST.get('quantity'))
    product_id = request.POST.get('id')
    product = Product.objects.get(id=product_id)
    if product.quantity >= quantity:
        cart = Cart.objects.get(user_id=request.user.id , product_id=product_id)
        cart.quantity = quantity
        cart.save()
        messages.success(request,'Quantity updated successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,'Not enough product in stock')
        return redirect(request.META.get('HTTP_REFERER'))
    
def logout_view(request):
    logout(request)
    return redirect('index') 

def rating(request):
    rat = request.POST.get('rat')
    product_id = request.POST.get('product_id')
    rating = Rating.objects.create(stars=rat,product_id=product_id,user_id=request.user.id)
    rating.save()
    messages.success(request,'Ratings given successfully')
    return redirect(request.META.get('HTTP_REFERER'))