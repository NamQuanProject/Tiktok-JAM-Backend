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


    def getCategoryRec(self, query):      
        context = ", ".join(self.unique_categories)
        style_prompt = f"""
        Imagine you are a classifier of the query from customers of what they want belongs to which category or categories and styles.
        It can be more than one category to specify and answer in lowercase.
        These are the categories you have in lowercase: [{context}].

        Also, classify the style if mentioned.
        Here is the style list:
        {self.styles}
        Please give me a short and concise answer in just JSON format with the keys 'categories', 'styles',
        Question: {query}

        Category and style you think that query belongs to is:
        Answer:
        """
        text_response = get_rec(prompt=style_prompt)
        text_response = process_response(text_response)
        print(text_response)
        categories_of_interest = json.loads(text_response)
        return categories_of_interest







    def recommend_products(self, categories):
        recommended_products = []
        
        for product in self.products:
            product_category = product["category"]["type"].lower()
            product_style = product["category"]["style"]
            product_style = [product.lower() for product in product_style]
            
            if product_category in [category.lower() for category in categories["categories"]]:
                if categories["styles"]:
                    intersection = set(categories["styles"]).intersection(product_style)
                    if len(intersection) / len(categories["styles"]) > 0.5:
                        recommended_products.append(product)
                else:

                    recommended_products.append(product) 
        recommended_products = sorted(recommended_products, key=lambda x: x["rating"]["stars"], reverse=True)
        return recommended_products



query = "I want a gift which is vintage and look nice for my girlfriend"
rec = RecommendProducts()
categories_of_interest = rec.getCategoryRec(query=query)
rec_products = rec.recommend_products(categories_of_interest)
print(rec_products[:10])
print(len(rec_products))



history  = {



}