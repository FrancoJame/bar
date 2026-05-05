from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    MANAGER = 'MANAGER'
    STAFF = 'STAFF'
    CUSTOMER = 'CUSTOMER'
    
    ROLE_CHOICES = [
        (MANAGER, 'Manager'),
        (STAFF, 'Staff'),
        (CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
