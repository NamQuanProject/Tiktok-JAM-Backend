from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from product.models import Product, Category, Style
from user.models import User
from recommend.RecommendFunctions.recommend import RecommendProducts
import json
import random

# Create your views here.

rec = RecommendProducts()

@csrf_exempt
# def AI_recommend_products(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         query = data["query"]
#         AI_categories = rec.getCategoryRec(query=query)
#         user = request.user

#         # Fetch user's shopping history
#         shopping_history = get_user_shopping_history(user)

#         recommended_products = []
#         products = Product.objects.all()

#         for product in products:
#             product_category = product.category.name.lower()
#             product_styles = [style.name.lower() for style in product.styles.all()]

#             if product_category in [category.lower() for category in AI_categories["categories"]]:
#                 if not AI_categories["styles"]:
#                     shop_his_category = shopping_history["categories"]
#                     history_style = shop_his_category[product_category]
#                     AI_categories["styles"] = list()
#                     key_with_highest_value = max(history_style, key=history_style.get)
#                     count = history_style[key_with_highest_value]

#                     three_quarters_count = count * 0.75
#                     for key, count in history_style.items():
#                         if count > three_quarters_count:
#                             AI_categories["styles"].append(key)

#                 intersection = set(AI_categories["styles"]).intersection(product_styles)
#                 if len(intersection) / len(AI_categories["styles"]) > 0.5:
#                     if AI_categories["price"]:
#                         if (AI_categories["price"] - 5) * 100 < product.priceCents < (AI_categories["price"] + 5) * 100:
#                             recommended_products.append(product)
#                     else:
#                         recommended_products.append(product)

#         recommended_products = sorted(recommended_products, key=lambda x: x.rating['stars'], reverse=True)

#         # Convert to a list of dictionaries for JSON response
#         recommended_products_data = [
#                 {   
#                     "id" : product.id,
#                     "name": product.name,
#                     "category": product.category.name,
#                     "styles": [style.name for style in product.styles.all()],
#                     "priceCents": product.priceCents,
#                     "rating_stars": product.rating['stars'],
#                 }
#                 for product in recommended_products
#         ]

#         return JsonResponse(recommended_products_data, safe=False)

#     return JsonResponse({"error": "Invalid HTTP method"}, status=400)

def get_user_shopping_history(user):
    shopping_history=  {
      "new_user" : True,
      "categories": {
        "clothing": {
          "vintage": 10,
          "hipster": 6,
          "bohemian": 6,
          "preppy": 6,
          "jeans": 8,
          "men": 6,
          "streetwear": 5,
          "business casual": 3,
          "artsy": 3,
          "blazers": 3,
          "women": 6,
          "ethnic": 2,
          "grunge": 2,
          "casual": 2,
          "scarves": 2,
          "kids": 7,
          "gothic": 3,
          "retro": 3,
          "loungewear": 6,
          "blouses": 3,
          "formal": 2,
          "punk": 2,
          "sweaters": 2,
          "athleisure": 3,
          "minimalist": 3,
          "tops": 3
        }
      },
      "average_price": 16
    }
    return shopping_history

# @csrf_exempt
# def checkbox_category_recommend(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         categories = data["checkbox_categories"]
#         shopping_history = get_user_shopping_history(request.user)  # Assuming this function retrieves shopping history

#         recommended_products = []
#         products = Product.objects.all()

#         for product in products:
#             product_category = product.category.name.lower()
#             product_styles = [style.name.lower() for style in product.styles.all()]

#             if product_category == categories["category"].lower():
#                 shop_his_category = shopping_history["categories"]
#                 history_style = shop_his_category.get(product_category, {})  # Handle case when category not found
#                 key_with_highest_value = max(history_style, key=history_style.get)
#                 count = history_style[key_with_highest_value]

#                 three_quarters_count = count * 0.75
#                 for key, count in history_style.items():
#                     if count > three_quarters_count and key not in categories["styles"]:
#                         categories["styles"].append(key)

#                 intersection = set(categories["styles"]).intersection(product_styles)
#                 if len(intersection) / len(categories["styles"]) >= 0.5:
#                     if categories["low_price"] * 100 < product.priceCents < categories["high_price"] * 100:
#                         recommended_products.append(product)

#         recommended_products = sorted(recommended_products, key=lambda x: x.rating["stars"], reverse=True)
#         print(len(recommended_products))
#         recommended_products_data = [
#                 {   
#                     "id" : product.id,
#                     "name": product.name,
#                     "category": product.category.name,
#                     "styles": [style.name for style in product.styles.all()],
#                     "priceCents": product.priceCents,
#                     "rating_stars": product.rating['stars'],
#                 }
#                 for product in recommended_products
#         ]

#         return JsonResponse(recommended_products_data, safe=False)

#     return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def shopping_history_recommend(request):
    if request.method == "POST":
        shopping_history = get_user_shopping_history(request.user)
        recommended_products = []
        products = Product.objects.all()
        if shopping_history["new_user"]:
            highest_rated_products = sorted(products, key=lambda x: x.rating["stars"], reverse=True)
            top_n = 20
            highest_rated_products = highest_rated_products[:top_n]
            num_recommendations = 10  
            recommended_products = random.sample(highest_rated_products, min(len(highest_rated_products), num_recommendations))

        
        else:
            category_preferences = shopping_history.get("categories", {})
            avg_price = shopping_history.get("average_price", 0)
            

            for product in products:
                product_category = product.category.name.lower()
                product_styles = [style.name.lower() for style in product.styles.all()]

                if product_category in category_preferences:
                    preferred_styles = category_preferences[product_category]
                    top_styles = sorted(preferred_styles, key=preferred_styles.get, reverse=True)
                    intersection = set(top_styles).intersection(product_styles)
                    if intersection:
                        if (avg_price - 10) * 100 < product.priceCents < (avg_price + 5000) * 100:
                            recommended_products.append(product)

            recommended_products = sorted(recommended_products, key=lambda x: x.rating["stars"], reverse=True)
            print(len(recommended_products))
        recommended_products_data = [
                {   
                    "id" : product.id,
                    "name": product.name,
                    "category": product.category.name,
                    "styles": [style.name for style in product.styles.all()],
                    "price_cents": product.priceCents,
                    "rating_stars": product.rating['stars'],
                }
                for product in recommended_products
        ]

        return JsonResponse(recommended_products_data, safe=False)
    
@csrf_exempt
def combined_recommend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        AI_query = data["AI_query"]
        categories = data["checkbox_categories"]

        shopping_history = get_user_shopping_history(request.user)
        shop_his_category = shopping_history["categories"]
        AI_categories = rec.getCategoryRec(query=AI_query)
        if categories["category"] not in AI_categories["categories"]:
            AI_categories["categories"].append(categories["category"])
        
        combined_styles = list(set(categories["styles"] + AI_categories["styles"]))



        categories["category"] = list(AI_categories["categories"])
        categories["styles"] = combined_styles


        recommended_products = []
        products = Product.objects.all()

        for product in products:
            product_category = product.category.name.lower()
            product_styles = [style.name.lower() for style in product.styles.all()]

            if product_category in [category.lower() for category in categories["category"]]:
                history_style = shop_his_category.get(product_category, {}) 
                
                if history_style:
                    key_with_highest_value = max(history_style, key=history_style.get)
                    count = history_style[key_with_highest_value]
                    three_quarters_count = count * 0.75
                    for key, count in history_style.items():
                        if count > three_quarters_count and key not in categories["styles"]:
                            categories["styles"].append(key)

                intersection = set(categories["styles"]).intersection(product_styles)
                if len(intersection) / len(categories["styles"]) >= 0.5:
                    if categories["low_price"] * 100 < product.priceCents < categories["high_price"] * 100:
                        recommended_products.append(product)

            recommended_products = sorted(recommended_products, key=lambda x: x.rating["stars"], reverse=True)
        recommended_products_data = [
                {   
                    "id" : product.id,
                    "name": product.name,
                    "category": product.category.name,
                    "styles": [style.name for style in product.styles.all()],
                    "price_cents": product.priceCents,
                    "rating_stars": product.rating['stars'],
                }
                for product in recommended_products
        ]

        return JsonResponse(recommended_products_data, safe=False)
    return JsonResponse({"error": "Method not allowed"}, status=405)

        
        
        







        
