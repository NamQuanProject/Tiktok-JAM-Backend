import os
import django
import json

# Set the environment variable to your project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TTJ_BE.settings')

# Initialize Django
django.setup()

import json
from user.models import User
from product.models import Product, Category, Style

def json_to_db():
    with open('style.json') as file: 
        data = json.load(file)
        for category, styles in data.items():
            category_instance = Category.objects.create(name=category.lower())
            category_instance.save()    
            for style in styles:
                style_instance, created = Style.objects.get_or_create(name=style.lower())
                style_instance.save()
                category_instance.style.add(style_instance) 
        
    
    with open('products.json') as file:
        data = json.load(file)
        for product in data["products"]:
            category_instance = Category.objects.get(name=product['category']['type'].lower())
            product_instance = Product.objects.create(
                id=product['id'],
                image=product.get('image', 'default_image_path_or_url'),
                name=product['name'],
                rating=product['rating'],
                priceCents=product['priceCents'],
                keywords=product['keywords'],
                category=category_instance
            )
            product_instance.save()
            for style in product['category']['style']:
                style_instance, created = Style.objects.get_or_create(name=style.lower())
                product_instance.style.add(style_instance)


        
json_to_db()
