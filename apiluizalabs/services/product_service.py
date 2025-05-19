import os
import random

import requests
from faker import Faker

from ..models import mem_products

fake = Faker("pt_BR")


class ProductAPIService:
    def get_all(self):
        response = requests.get(os.getenv("PRODUCTS_API_URL"))
        if response.status_code == 200:
            return response.json()
        return []

    def get(self, product_id):
        response = requests.get(f"{os.getenv('PRODUCTS_API_URL')}/{product_id}")
        if response.status_code == 200:
            return response.json()
        return None

    def exists(self, product_id):
        response = requests.get(f"{os.getenv('PRODUCTS_API_URL')}/{product_id}")
        return response.status_code == 200


class ProductMockService:
    def get_all(self):
        return list(mem_products.values())

    def get(self, product_id):
        return mem_products.get(product_id)

    def exists(self, product_id):
        return product_id in mem_products

    def create_mock_products(self, total=100):
        size = len(mem_products)
        for _ in range(total):
            size += 1
            product_id = f"PROD-{size:06}"
            mem_products[product_id] = {
                "id": product_id,
                "title": fake.word().capitalize(),
                "image": f"image_{size:06}.jpg",
                "price": round(random.uniform(0.1, 1000), 2),
                "brand": fake.company().capitalize(),
                "reviewScore": round(random.uniform(0, 10), 1),
            }
        return list(mem_products.values())


def get_product_service():
    if os.getenv("PRODUCTS_SOURCE") == "api":
        return ProductAPIService()
    return ProductMockService()
