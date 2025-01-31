from django.db import models
from django.contrib.auth.models import AbstractUser
class Admin(AbstractUser):
    username = models.CharField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    #REQUIRED_FIELDS = ['email']
   
    
  
