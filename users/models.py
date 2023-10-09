from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

# custom user manager\
class CustomUserManager(BaseUserManager):
    # create user 
    def create_user(self, firstname, lastname, username, email, password, **extra_fields):

        if not firstname:
            raise ValueError(_("Firstname address is required"))
        if not lastname:
            raise ValueError(_("Lastname address is required"))
        if not username:
            raise ValueError(_("Username address is required"))
        if not email:
            raise ValueError(_("Email address is required"))

        email = self.normalize_email(email)
        user = self.model(
            firstname=firstname, 
            lastname=lastname,
            username=username, 
            email=email
            )

        if password is None:
            raise ValueError(_("Password is required"))
        
        user.set_password(password)
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user 
    
    # create super user 
    def create_superuser(self, username, email, password, **extra_fields):

        user = self.model(
            username=username,
            email=email
        )
        user.is_superuser = True
        user.is_staff = True
        
        if password is None:
            raise ValueError(_("Password is required"))
        
        user.set_password(password)
        user.save()
        return user 
    
# user model 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20, null=False, blank=False)
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["firstname", "lastname", "email"]

    objects = CustomUserManager()

    def __str__(self):
        return  f"{self.username}"


