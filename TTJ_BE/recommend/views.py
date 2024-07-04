from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from product.models import Product, Category, Style
from user.models import User
from recommend.RecommendFunctions.recommend import RecommendProducts
import json

# Create your views here.

rec = RecommendProducts()

@csrf_exempt
def AI_recommend_products(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data["query"]
        AI_categories = rec.getCategoryRec(query=query)
        user = request.user

        # Fetch user's shopping history
        shopping_history = get_user_shopping_history(user)

        recommended_products = []
        products = Product.objects.all()

        for product in products:
            product_category = product.category.name.lower()
            product_styles = [style.name.lower() for style in product.styles.all()]

            if product_category in [category.lower() for category in AI_categories["categories"]]:
                if not AI_categories["styles"]:
                    shop_his_category = shopping_history["categories"]
                    history_style = shop_his_category[product_category]
                    AI_categories["styles"] = list()
                    key_with_highest_value = max(history_style, key=history_style.get)
                    count = history_style[key_with_highest_value]

                    three_quarters_count = count * 0.75
                    for key, count in history_style.items():
                        if count > three_quarters_count:
                            AI_categories["styles"].append(key)

                intersection = set(AI_categories["styles"]).intersection(product_styles)
                if len(intersection) / len(AI_categories["styles"]) > 0.5:
                    if AI_categories["price"]:
                        if (AI_categories["price"] - 5) * 100 < product.priceCents < (AI_categories["price"] + 5) * 100:
                            recommended_products.append(product)
                    else:
                        recommended_products.append(product)

        recommended_products = sorted(recommended_products, key=lambda x: x.rating['stars'], reverse=True)

        # Convert to a list of dictionaries for JSON response
        recommended_products_data = [
            {
                "name": product.name,
                "category": product.category.name,
                "styles": [style.name for style in product.styles.all()],
                "price_cents": product.priceCents,
                "rating_stars": product.rating['stars'],
            }
            for product in recommended_products
        ]

        return JsonResponse(recommended_products_data, safe=False)

    return JsonResponse({"error": "Invalid HTTP method"}, status=400)

def get_user_shopping_history(user):
    shopping_history = {
        "categories": {
            "clothing": {"vintage": 25, "kids": 10, "casual": 20, "sporty": 15, "formal": 5},
            "gifts": {"trendy": 30, "classic": 10, "chic": 5},
            "electronics": {"user-friendly": 15, "compact": 10, "sleek": 5},
            "beauty & personal care": {"trendy": 20, "industrial": 10},
            "home": {"modern": 10, "urban": 5}
        },
        "average_price": 20
    }
    return shopping_history

@csrf_exempt
def checkbox_category_recommend(request):
    if request.method == "POST":
        data = json.loads(request.body)
        categories = data["checkbox_categories"]
        shopping_history = get_user_shopping_history(request.user)  # Assuming this function retrieves shopping history

        recommended_products = []
        products = Product.objects.all()

        for product in products:
            product_category = product.category.name.lower()
            product_styles = [style.name.lower() for style in product.styles.all()]

            if product_category == categories["category"].lower():
                shop_his_category = shopping_history["categories"]
                history_style = shop_his_category.get(product_category, {})  # Handle case when category not found
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
        print(len(recommended_products))
        # Prepare JSON response
        recommended_products_data = [
            {
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

@csrf_exempt
def shopping_history_recommend(request):
    if request.method == "POST":
        shopping_history = get_user_shopping_history(request.user)
        recommended_products = []
        category_preferences = shopping_history.get("categories", {})
        avg_price = shopping_history.get("average_price", 0)

        products = Product.objects.all()

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
                    "name": product.name,
                    "category": product.category.name,
                    "styles": [style.name for style in product.styles.all()],
                    "price_cents": product.priceCents,
                    "rating_stars": product.rating['stars'],
                }
                for product in recommended_products
            ]

        return JsonResponse(recommended_products_data, safe=False)