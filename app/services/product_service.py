# TODO: refatorar este service

import os
import random
import requests
from faker import Faker
from typing import Dict, List, Optional


PRODUCTS_SOURCE = os.getenv("PRODUCTS_SOURCE", "api")
PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL", None)

fake = Faker("pt_BR")

# Dict memmoria para armazenar produtos mockados
_mock_products: Dict[str, dict] = {}


def _generate_mock_products(num_products=100) -> None:
    categories = [
        "Brinquedos",
        "Beleza",
        "Casa",
        "Esportes",
        "Eletronicos",
        "Livros",
        "Roupas",
    ]

    brands = ["Marca A", "Marca B", "Marca C", "Marca D", "Marca E", "Marca F"]

    for i in range(1, num_products + 1):
        product_id = f"prod-{i}"
        _mock_products[product_id] = {
            "id": product_id,
            "title": f"{random.choice(categories)} - {fake.word().capitalize()} {fake.word().capitalize()}",
            "image": f"img{i}.jpg",
            "price": round(random.uniform(10.0, 1000.0), 2),
            "brand": random.choice(brands),
            "reviewScore": (
                round(random.uniform(1.0, 5.0), 1) if random.random() > 0.2 else None
            ),
        }


def get_all_products() -> List[dict]:
    if PRODUCTS_SOURCE == "api":
        try:
            response = requests.get(PRODUCTS_API_URL)
            if response.status_code == 200:
                return response.json()
            else:
                # TODO: tratar erros de conexoo e outros
                # Em caso de falha, usa mock como fallback (apenas para testes)
                print(f"Erro ao obter produtos da API: {response.status_code}")
                
                return list(_mock_products.values())
        except Exception as e:
            print(f"Erro ao conectar com a API de produtos: {str(e)}")
            
            return list(_mock_products.values())
    else:
        # TODO: teste remover
        # Se nao existir produtos mockados, criar novos
        if not _mock_products:
            _generate_mock_products()
       
        return list(_mock_products.values())


def get_product(product_id: str) -> Optional[dict]:
    if PRODUCTS_SOURCE == "api":
        try:
            response = requests.get(f"{PRODUCTS_API_URL}/{product_id}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                # TODO: tratar erros de conexao
                print(f"Erro ao obter produto da API: {response.status_code}")
                
                return _mock_products.get(product_id)
        except Exception as e:
            print(f"Erro ao conectar com a API de produtos: {str(e)}")
           
            return _mock_products.get(product_id)
    else:
        if not _mock_products:
            _generate_mock_products()
        
        return _mock_products.get(product_id)


def create_mock_products(total: int) -> list[dict]:
    if PRODUCTS_SOURCE == "api":
        raise Exception("Não é possível criar mocks quando a fonte é API externa")
    for i in range(total):
        product_id = f"mock-{len(_mock_products)+1}"
        _mock_products[product_id] = {
            "id": product_id,
            "title": f"Produto Mock {len(_mock_products)+1}",
            "image": f"image_{len(_mock_products)+1}.jpg",
            "price": round(random.uniform(10.0, 1000.0), 2),
            "brand": random.choice([
                "Nike", "Adidas", "Puma", "Reebok", "Fila", "Mizuno"
            ]),
            "reviewScore": round(random.uniform(1.0, 10.0), 2)
        }
    return list(_mock_products.values())

# Inicializa os prods mockados
if PRODUCTS_SOURCE == "mock":
    _generate_mock_products()
