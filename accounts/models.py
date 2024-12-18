from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('dealer', 'Dealer'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES,
        default='customer'  # Set default role to 'customer'
    )

     # Override the set_password method to store the password in plain text
    def set_password(self, raw_password):
        self.password = raw_password  # Store the password as plain text (for testing purposes)

    # Add related_name to avoid conflicts with the default 'User' model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom reverse relation for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Custom reverse relation for permissions
        blank=True
    )
