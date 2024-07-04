import json
import torch
import openai
from model import get_rec, process_response



class RecommendProducts():
    def __init__(self):
        with open("products.json") as file:
            data = json.load(file)
            self.products = data["products"]
        

        with open("style.json") as file:
            self.styles = json.load(file)



        self.unique_categories = set()
        for ind, product in enumerate(self.products):
            if "category" in product:  
                category  = product["category"]
                self.unique_categories.add(category["type"])
        self.category_context = ", ".join(self.unique_categories)

        self.styles_context = ""
        for style in self.styles:
            self.styles_context += f"{style}: {self.styles[style]}\n"

    def getCategoryRec(self, query):      
        style_prompt = f"""
        Imagine you are a classifier of the query from customers of what they want belongs to which category or categories and styles.
        It can be more than one category to specify and answer in lowercase.
        These are the categories you have in lowercase: [{self.category_context}].

        Also, classify the price and style if mentioned 
        This is important! Remember that if the question does not mentioned about price or styles do not put anything about them in the answer!
        Here is the style list:
        {self.styles_context}

        
        Please give me a short and concise answer in just JSON format with the keys 'categories', 'styles', 'price' in just a float number,
        
        Question: {query}
        Category and style and price you think that query belongs to is:
        Answer:
        """
        print(style_prompt)
        text_response = get_rec(prompt=style_prompt)
        text_response = process_response(text_response)
        print(text_response)
        categories_of_interest = json.loads(text_response)
        return categories_of_interest

    def AI_recommend_products(self, AI_categories, shopping_history):
        recommended_products = []
        for product in self.products:
            product_category = product["category"]["type"].lower()
            product_style = product["category"]["style"]
            product_style = [product.lower() for product in product_style]
            
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
                
                
                    
                intersection = set(AI_categories["styles"]).intersection(product_style)
                if len(intersection) / len(AI_categories["styles"]) > 0.5:
                    if AI_categories["price"]:
                        if (AI_categories["price"] - 5) * 100 < product["priceCents"] < (AI_categories["price"] + 5) * 100:
                            recommended_products.append(product)
                    else: 
                        recommended_products.append(product)
        recommended_products = sorted(recommended_products, key=lambda x: x["rating"]["stars"], reverse=True)
        return recommended_products


    def checkbox_category_recommend(self, categories, shopping_history):
        recommended_products = []

        for product in self.products:
            product_category = product["category"]["type"].lower()
            product_style = product["category"]["style"]
            product_style = [product.lower() for product in product_style]
            
            if product_category == categories["category"]:
                shop_his_category = shopping_history["categories"]
                history_style = shop_his_category[product_category]
                key_with_highest_value = max(history_style, key=history_style.get)
                count = history_style[key_with_highest_value]
                
                three_quarters_count = count * 0.75
                for key, count in history_style.items():
                    if count > three_quarters_count and key not in categories["styles"]:
                        categories["styles"].append(key)
                intersection = set(categories["styles"]).intersection(product_style)
                if len(intersection) / len(categories["styles"]) >= 0.5:
                    if categories["low_price"] * 100 < product["priceCents"] < categories["high_price"] * 100:
                        recommended_products.append(product)
                    
        recommended_products = sorted(recommended_products, key=lambda x: x["rating"]["stars"], reverse=True)
        return recommended_products
        
    


    def shopping_history_recommend(self, shopping_history):
        recommended_products = []
        category_preferences = shopping_history["categories"]
        avg_price = shopping_history["average_price"]

        for product in self.products:
            product_category = product["category"]["type"].lower()
            product_styles = [style.lower() for style in product["category"]["style"]]

            if product_category in category_preferences:
                preferred_styles = category_preferences[product_category]
                top_styles = sorted(preferred_styles, key=preferred_styles.get, reverse=True)
                intersection = set(top_styles).intersection(product_styles)
                if intersection:
                    if (avg_price - 10) * 100 < product["priceCents"] < (avg_price + 10) * 100:
                        recommended_products.append(product)
        
        recommended_products = sorted(recommended_products, key=lambda x: x["rating"]["stars"], reverse=True)
        return recommended_products


"""



shopping_history = {
    "categories": [
        "clothing": {"vintage" : 25, "kids" : 10},
        "gifts": {"trendy" : 30, "..." : ...},
    ]
    "average_price" : ... 
}
"""

check_box_category = {
    "low_price": 0,
    "high_price": 500,
    "category": "clothing",
    "styles" : ["vintage", "casual", "dresses"]
}

query = "I want to buy gifts as clothing for my boy friend"
user1_shopping_history = {
    "new_user" : False,
    "categories": {
        "clothing": {"vintage": 25, "kids": 10, "casual": 20, "sporty": 15, "formal": 5},
        "gifts": {"trendy": 30, "classic": 10, "chic": 5},
        "electronics": {"user-friendly": 15, "compact": 10, "sleek": 5},
        "beauty & personal care": {"trendy": 20, "industrial": 10},
        "home": {"modern": 10, "urban": 5}
    },
    "average_price": 50
}



# categories_of_interest = {
#     "categories": ["gifts", "clothing"],
#     "styles": None,
#     "price" : None,
# }

rec = RecommendProducts()
# categories_of_interest = rec.getCategoryRec(query=query)
rec_products = rec.shopping_history_recommend(shopping_history)
print(rec_products[:10])
print(len(rec_products))



