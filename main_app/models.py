from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin" 
        CUSTOMER = "customer", "Customer"  

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,  
    )
    
    class Meta:
        db_table = "users"  
    
    def __str__(self):
        return f'{self.username} ({self.role})'  

class Call(models.Model):
    class Status(models.TextChoices):
        SOLVED = "solved", "Solved"
        WORKING = "working", "Working on it"
        PROBLEM = "problem", "Problem"
    
    created_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=9999)
    status = models.CharField(  
        max_length=20,
        choices=Status.choices,
        default=Status.PROBLEM
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    
    class Meta:
        db_table = "calls"
    
    def __str__(self):
        return f'Call #{self.id} - {self.status}'

class Message(models.Model):
    created_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=9999)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    call = models.ForeignKey(Call, on_delete=models.CASCADE)  
    
    class Meta:
        db_table = "messages"
    
    def __str__(self):
        return f'Message #{self.id} '