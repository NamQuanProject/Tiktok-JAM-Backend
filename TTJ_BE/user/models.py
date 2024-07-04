from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from product.models import Product
# Create your models here.

class User(AbstractBaseUser):
    is_new = models.BooleanField(default=True)
    avarage_price = models.FloatField(default=0)
    product = models.ManyToManyField(Product, related_name='users')