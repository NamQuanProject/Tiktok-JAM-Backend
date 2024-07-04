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
        If not mention price or style do not put it in the answer !
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

    def AI_recommend_products(self, AI_categories):
        recommended_products = []
        
        for product in self.products:
            product_category = product["category"]["type"].lower()
            product_style = product["category"]["style"]
            product_style = [product.lower() for product in product_style]
            
            if product_category in [category.lower() for category in AI_categories["categories"]]:
                if AI_categories["styles"]:
                    intersection = set(AI_categories["styles"]).intersection(product_style)
                    if len(intersection) / len(AI_categories["styles"]) > 0.5:
                        if AI_categories["price"]:
                            if (AI_categories["price"] - 5) * 100 < product["priceCents"] < (AI_categories["price"] + 5) * 100:
                                recommended_products.append(product)
                        else: 
                            recommended_products.append(product)

                else:

                    recommended_products.append(product) 
        recommended_products = sorted(recommended_products, key=lambda x: x["rating"]["stars"], reverse=True)
        
        return recommended_products


    def checkbox_category_recommend(categories):
        pass

"""
check_box_category:
{
    low_price:
    high_price:
    category: str
    style : [str, str, ...]
}
"""


query = "I want to buy gifts as clothing for my boy friend"
rec = RecommendProducts()
categories_of_interest = rec.getCategoryRec(query=query)
rec_products = rec.recommend_products(categories_of_interest)
print(rec_products[:10])
print(len(rec_products))



