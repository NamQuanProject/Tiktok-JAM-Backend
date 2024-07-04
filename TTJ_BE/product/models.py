from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    style = models.ManyToManyField('Style', related_name='categories')

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=True)
    image = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    rating = models.JSONField(default=dict)
    priceCents = models.IntegerField()
    keywords = models.JSONField(default=list)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    style = models.ManyToManyField('Style', related_name='products')

class Style(models.Model):
    name = models.CharField(max_length=100)
