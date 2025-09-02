from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin" 
        Coustmore = "user", "User"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.User,  
    )

class Call(models.Model):
    created_date=models.DateField()