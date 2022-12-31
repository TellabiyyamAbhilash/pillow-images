from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from users.managers import UserManager
from . import constants as user_constants

def upload_path(instance, filename):
    return '/'.join(['images', str(instance.id), filename])


class User(AbstractUser):
    username = None # remove username field, we will use email as unique identifier
    first_name = models.CharField(max_length=50,default="",null=False,blank=False) 
    last_name = models.CharField(max_length=50,default="",null=False,blank=False)
    email = models.EmailField(unique=True,null=False,blank=False, db_index=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.PositiveSmallIntegerField(choices=user_constants.USER_TYPE_CHOICES,default=user_constants.CUSTOMER)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email


class Images(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    input_image = models.ImageField(null=False,blank=False,upload_to=upload_path)
    Thumbnail  =models.ImageField(null=True,blank=True)
    medium = models.ImageField(null=True,blank=True)
    large = models.ImageField(null=True,blank=True)
    grayscale = models.ImageField(null=True,blank=True)
