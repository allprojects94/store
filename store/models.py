from django.db import models
from django.core.exceptions import ValidationError  # Import ValidationError
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=False)
    dealer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Cascade delete categories with the dealer

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)  # Ensure quantity cannot be negative
    color = models.CharField(max_length=50, blank=True)
    image_url = models.URLField(blank=True)  # For storing an image URL
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Cascade delete products with the category
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('user', 'product')  # Ensures a user can only have one entry per product in the cart

    def __str__(self):
        return f"{self.user.username}'s cart"
