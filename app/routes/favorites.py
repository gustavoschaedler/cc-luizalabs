from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProductFavorite, ProductOut
from app.auth import authenticate
from app.models import mem_clients
from app.services.product_service import get_product
import os


PRODUCTS_SOURCE = os.getenv("PRODUCTS_SOURCE", "api")
PRODUCTS_API_URL = os.getenv("PRODUCTS_API_URL", None)

router = APIRouter(prefix="/favorites", tags=["Favoritos"])

def get_client_or_404(email: str):
    client = mem_clients.get(email)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return client

def check_product_exists(product_id: str):
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto inexistente")
    return product

def check_favorite_not_exists(client, product_id: str):
    if product_id in client["favorites"]:
        raise HTTPException(status_code=400, detail="Produto ja favoritado")

def check_favorite_exists(client, product_id: str):
    if product_id not in client["favorites"]:
        raise HTTPException(status_code=400, detail="Produto nao esta nos favoritos")

@router.get("/{email}", response_model=list[ProductOut])
def get_favorites(email: str, _=Depends(authenticate)):
    client = get_client_or_404(email)
    favorites = []
    for pid in client["favorites"]:
        product = get_product(pid)
        if product:
            favorites.append(product)
    return favorites

@router.post("/{email}", status_code=201)
def add_favorite(email: str, fav: ProductFavorite, _=Depends(authenticate)):
    client = get_client_or_404(email)
    check_product_exists(fav.product_id)
    check_favorite_not_exists(client, fav.product_id)
    client["favorites"].append(fav.product_id)
    return {"msg": "Produto adicionado aos favoritos com sucesso"}

@router.delete("/{email}/{product_id}")
def remove_favorite(email: str, product_id: str, _=Depends(authenticate)):
    client = get_client_or_404(email)
    check_favorite_exists(client, product_id)
    client["favorites"].remove(product_id)
    return {"msg": "Produto removido dos favoritos com sucesso"}
