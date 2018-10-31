from django.db import models
from django.contrib.auth.models import AbstractUser
from introduce.models import Department
# Create your models here.

class NewUser(AbstractUser):
    profile = models.CharField(max_length=256,blank=True)
    avatar = models.ImageField(upload_to='AvatarImage',default='AvatarImage/default.png')
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True)
    nickname = models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return self.username

