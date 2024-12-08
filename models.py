from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    access_level = models.JSONField()  # Stores access details for data lakes and warehouses