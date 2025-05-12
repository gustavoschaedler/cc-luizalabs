from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProductOut, ProductCreate
from app.auth import authenticate
from app.models import products
from typing import List

router = APIRouter(prefix="/products", tags=["Produtos"])


@router.get("/", response_model=List[ProductOut])
def get_all_products(_=Depends(authenticate)):
    """
    Retorna todos os produtos cadastrados.
    """
    return list(products.values())


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, _=Depends(authenticate)):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    return products[product_id]


@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, _=Depends(authenticate)):
    # Gera um novo ID para o produto
    product_id = f"prod-{len(products) + 1}"

    # Verifica se ID ja existe, gera um novo se necessario
    while product_id in products:
        product_id = f"prod-{int(product_id.split('-')[1]) + 1}"

    # Cria produto no dict
    products[product_id] = {
        "id": product_id,
        "title": product.title,
        "image": product.image,
        "price": product.price,
        "brand": product.brand,
        "reviewScore": product.reviewScore,
    }

    return products[product_id]
