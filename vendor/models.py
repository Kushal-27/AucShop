from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import User
# Create your models here.
#user table
class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,name,phone_number, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        if not password:
            raise ValueError('Password is not provided')
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            phone_number = phone_number,

            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email, password, name,phone_number, **extrafields):
        extrafields.setdefault('is_superuser', False)
        extrafields.setdefault('is_staff', False)
        extrafields.setdefault('is_active', False)
        return self._create_user(email, password, name, phone_number, **extrafields)

    def create_superuser(self, email, password,name,phone_number, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser',True)
        return self._create_user(email, password, name, phone_number,**extrafields)


class Vendor(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=200)
    
    email = models.EmailField(db_index = True,unique=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20,unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['vendor_name','vendor_phone_number']
    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
    
    groups = models.ManyToManyField(Group, related_name='vendor_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='vendor_permissions')


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
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions_selling')
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