import json

with open("products.json") as file:
    data = json.load(file)
    products = data["products"]

unique_categories = set()


for ind, product in enumerate(products):
    if "category" in product:
        unique_categories.add(product["category"])


for categories in unique_categories:
    print(categories)