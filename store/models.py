from django.db import models
from django.core.exceptions import ValidationError  # Import ValidationError
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    color = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        # Ensures that the quantity can't be negative
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative.')

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product')  # Ensures a user can only have one entry per product in the cart

    def __str__(self):
        return f"{self.user.username}'s cart"
