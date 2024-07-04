from django.db import models
import uuid

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    styles = models.ManyToManyField('Style', related_name='categories')

    def __str__(self):
        return self.name

# Style Model
class Style(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    rating = models.JSONField(default=dict)
    priceCents = models.IntegerField()
    keywords = models.JSONField(default=list)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    styles = models.ManyToManyField(Style, related_name='products')

    def __str__(self):
        return self.name

# History Style Model
class HistoryStyle(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField()

    def __str__(self):
        return self.name

# History Category Model
class HistoryCategory(models.Model):
    name = models.CharField(max_length=100)
    styles = models.ManyToManyField(HistoryStyle, related_name='history_categories')

    def __str__(self):
        return self.name

# Shopping History Model
class ShoppingHistory(models.Model):
    categories = models.ManyToManyField(HistoryCategory, related_name="shopping_histories")

    def __str__(self):
        return f"Shopping History {self.id}"
