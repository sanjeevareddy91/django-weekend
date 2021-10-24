from django.db import models

# Create your models here.

class Register(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=15)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name 
        
    class Meta:
        db_table = 'register_info'