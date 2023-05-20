from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from vendor.models import Product, Order
import json

from datetime import datetime
from django.contrib import messages
import requests

# Create your views here.

def config(request):
    
    order = request.POST.get('order')
    
    address = request.POST.get('address')
    product_id, quantity = order.split('|')
    product = Product.objects.get(id=product_id)
    amount = int(quantity) * product.price
    return render(request, "config.html", {"amount": amount, "product_id": product_id,"quantity":quantity, "address":address})



def verify(request):   
    if request.method == 'POST':
        payload = json.loads(request.body)
        product_id = payload.get('product_id')
        quantity = payload.get('quantity')
        address = payload.get('address')
        # process the payload data here
        token = payload['token']
        amount = payload['amount']
        idx = payload['idx']

        url = "https://khalti.com/api/v2/payment/verify/"

        payload = {
            'token': token,
            'amount': amount
        }

        headers = {
            'Authorization': 'Key test_secret_key_b2c0ace018b742eea4beafffef01f5b9'
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        if response.status_code != 200:
            print('Payment verification failed:', response.content)
            return JsonResponse({'status': 'error'})
        else:
            # if the request is authenticated, save the data in the Order table
            # messages.success(request, "Payment Successfully")
            product = Product.objects.get(id=product_id)
            orders = Order.objects.create(quantity=quantity,order_status='Processing',customer_id=request.user.id,product_id=product_id,vendor_id = product.vendor_id,address=address)
            orders.save()
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

  