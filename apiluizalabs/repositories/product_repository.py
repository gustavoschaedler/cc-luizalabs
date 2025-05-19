import os
import random

import httpx
from faker import Faker

from apiluizalabs.models import mem_products

fake = Faker("pt_BR")


class ProductRepository:
    def __init__(self, source="mock", api_url=None):
        self.source = source
        self.api_url = api_url
        self.api_auth = os.getenv("PRODUCTS_API_AUTHORIZATION")

    def get_all(self):
        """Retorna todos os produtos"""
        if self.source == "mock":
            return list(mem_products.values())
        else:
            try:
                headers = {}
                if self.api_auth:
                    headers["Authorization"] = f"Bearer {self.api_auth}"
                response = httpx.get(self.api_url, headers=headers)
                if response.status_code == 200:
                    return response.json()
                return []
            except Exception:
                raise Exception("Erro ao acessar API de produtos")

    def get_by_id(self, product_id):
        """Retorna um produto pelo ID"""
        if self.source == "mock":
            return mem_products.get(product_id)
        else:
            try:
                headers = {}
                if self.api_auth:
                    headers["Authorization"] = f"Bearer {self.api_auth}"
                response = httpx.get(f"{self.api_url}/{product_id}", headers=headers)
                if response.status_code == 200:
                    return response.json()
                return None
            except Exception:
                raise Exception("Erro ao acessar API de produtos")

    def exists(self, product_id):
        """Verifica se um produto existe"""
        if self.source == "mock":
            return product_id in mem_products
        else:
            try:
                headers = {}
                if self.api_auth:
                    headers["Authorization"] = f"Bearer {self.api_auth}"
                response = httpx.get(f"{self.api_url}/{product_id}", headers=headers)
                return response.status_code == 200
            except Exception:
                raise Exception("Erro ao acessar API de produtos")

    def create_mock_products(self, total):
        """Cria produtos mockados (apenas para testes)"""
        if self.source != "mock":
            raise ValueError("Operação não suportada para API externa")

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
