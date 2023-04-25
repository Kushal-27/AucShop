from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
def index(request):
    return render(request, 'homee.html')

def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username = email, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')


    else:
        return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        full_name = request.POST['name']
        name_list = full_name.split()
        length = len(name_list)
        first_name = name_list[0]
        last_name = name_list[length-1]
        phone_number = request.POST['number']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already in use')
                return redirect('signup')
            else:
                user = User.objects.create_user(first_name=first_name,last_name= last_name, phone_number= phone_number, email=email,password=password1)
                user.save()
                messages.success(request,'Account created successfully! Please Login')
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')

        return redirect('login')
    else: 
        return render(request, 'register.html')

@login_required(login_url='/login')
def home(request):
    return render(request, 'homee.html')

def about(request):
    return render(request, 'aboutt.html')

def cart(request):
    return render(request,'cartt.html')

def auction(request):
    return render(request, 'auctionn.html')

def account(request):
    return render(request, 'accountt.html')

def products(request):
    return render(request, 'productt.html')