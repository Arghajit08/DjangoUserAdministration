import imp
from django.db import models

#used abstractbaseuser to inherit django internal user model
from django.contrib.auth.models import AbstractBaseUser

#created three user levels-Superadmin,Teacher,Student
class SuperAdmin(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    level=models.CharField(max_length=30)
    is_valid=models.BooleanField(default=True)
    
class Teacher(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    level=models.CharField(max_length=30)
    is_valid=models.BooleanField(default=True)

class Student(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    level=models.CharField(max_length=30)
    is_valid=models.BooleanField(default=True)

# Create your models here.
