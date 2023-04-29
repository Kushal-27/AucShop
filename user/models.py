from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager, Group, Permission
# Create your models here.
#user table
class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,first_name,last_name,phone_number, **extra_fields):
        if not email:
            raise ValueError('Email is not provided')
        if not password:
            raise ValueError('Password is not provided')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,

            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email, password, first_name,last_name,phone_number, **extrafields):
        extrafields.setdefault('is_superuser', False)
        extrafields.setdefault('is_staff', False)
        extrafields.setdefault('is_active', True)
        return self._create_user(email, password, first_name, last_name, phone_number, **extrafields)

    def create_superuser(self, email, password,first_name,last_name,phone_number, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser',True)
        return self._create_user(email, password, first_name, last_name, phone_number,**extrafields)


class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(db_index = True,unique=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_vendor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number']
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')