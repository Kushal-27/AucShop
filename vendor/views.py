
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from vendor.models import Product, Auction, Bid
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from vendor.models import Cart, Order, Vendor, Offer, Rating
from datetime import datetime
User = get_user_model()
# Create your views here.

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username = email, password=password, is_vendor = "True")
        
        if user is not None:
            auth.login(request,user)
            messages.success(request, 'Logged in Successfully')
            return redirect('vendor:vendorhome')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('vendor')
    return render(request, 'vendorlogin.html')

def register(request):
    if request.method == "POST":
        
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
        shopname = request.POST['shopname']
        pannumber = request.POST['pannumber']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already in use')
                return redirect('vendor:vendorsignup')
            else:
                user = User.objects.create_user(first_name=first_name,last_name= last_name, phone_number= phone_number, email=email,password=password1,is_vendor ="True")
                user.save()
                user = User.objects.get(email=email)
                vendor = Vendor.objects.create(shopname=shopname,pan_number=pannumber,user_id=user.id)
                vendor.save()
                messages.success(request,'Account created successfully! Please Login')
        else:
            messages.error(request,'Password not matching')
            return redirect('vendor:vendorsignup')

        return redirect('vendor:vendorlogin')
    return render(request, 'vendorsignup.html')
@login_required(login_url='/vendor/vendorlogin')
def vendorhome(request):
    vendor = Vendor.objects.get(user_id=request.user.id)
    order = Order.objects.filter(vendor_id=vendor.id)
    total = 0
    for ord in order:
        product = Product.objects.get(id = ord.product_id)
        total = total + ord.quantity*product.price

    total_orders = len(order)
    product = Product.objects.filter(vendor_id = vendor.id)
    n=0
    for prod in product:
        offer = Offer.objects.filter(product_id_id=prod.id)
        n = n+ len(offer)
    total_products = len(product)
    context = {'sales':total,'offers':n,'products':total_products,'orders':total_orders}
    return render(request,'dashboard.html',context)
@login_required(login_url='/vendor/vendorlogin')
def profile(request):
    user = User.objects.get(id=request.user.id)
    vendor = Vendor.objects.get(user_id=user.id)
    context = {'user':user,'vendor':vendor}
    return render(request,'vendoraccount.html',context)

@login_required(login_url='/vendor/vendorlogin')
def offer(request):
    vendor = Vendor.objects.get(user_id=request.user.id)
    product = Product.objects.filter(vendor_id=vendor.id)
    offers = []

    for prod in product:
        offer_queryset = Offer.objects.filter(product_id_id=prod.id)
        for offer in offer_queryset:
            offer.message = prod.name
            offers.append(offer)

    context = {'offers': offers}
    return render(request, 'vendoroffer.html', context)

@login_required(login_url='/vendor/vendorlogin')
def acceptoffer(request):
    id = request.POST.get('id')
    offer = Offer.objects.get(id = id)
    offer.status = "Accepted"
    offer.save()
    messages.success(request,"You have accepted the offer")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/vendor/vendorlogin')
def declineoffer(request):
    id = request.POST.get('id')
    offer = Offer.objects.get(id = id)
    offer.status = "Accepted"
    offer.save()
    messages.success(request,"You have decllined the offer")
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/vendor/vendorlogin')
def listproduct(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        offer = request.POST.get('offer')
        image = request.POST.get('image')
        vendor = Vendor.objects.get(user_id=request.user.id)
        product = Product.objects.create(name=name,description=description,quantity=quantity,price=price,offers=offer,product_picture=image,vendor_id=vendor.id)
        product.save()
        messages.success(request,'Product Added Successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'listproduct.html')

@login_required(login_url='/vendor/vendorlogin')
def createauction(request):
    if request.method == 'POST':
        # start_time_str = ''
        # end_time_str = ''
        vendor = Vendor.objects.get(user_id=request.user.id)
        item = request.POST.get('item')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')
        starting_bid = request.POST.get('starting_bid')
        reserve_price = request.POST.get('reserve_price')
        bid_increment = request.POST.get('bid_increment')
        
        start_time= request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        status = request.POST.get('status')
        
        auction = Auction.objects.create(item=item, description=description, product_picture=picture,current_bid=0, starting_bid=starting_bid,seller_id=vendor.id,reserve_price=reserve_price, bid_increment=bid_increment, start_time=start_time, end_time=end_time, status=status)
        
        auction.save()
        
        messages.success(request, 'Auction Created Successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'createauction.html')

@login_required(login_url='/vendor/vendorlogin')
def logoutt(request):
    
    logout(request)
    return redirect('index')