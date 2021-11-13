from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Register(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=25)
    mobile = models.CharField(max_length=10)
    address = models.TextField()
    profile_pic = models.FileField(blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name 
        
    class Meta:
        db_table = 'register_info'