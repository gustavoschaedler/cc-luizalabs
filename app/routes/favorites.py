import os

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.auth import authenticate
from app.models import mem_clients
from app.schemas import ProductFavorite, ProductOut
from app.schemas import FavoritesListOut  # ADICIONE ESTA LINHA
from app.services.product_service import get_product_service

router = APIRouter(prefix="/favorites", tags=["Favoritos"])


def get_client_or_404(email: str):
    client = mem_clients.get(email)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return client


product_service = get_product_service()


def check_product_exists(product_id: str):
    product = product_service.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto inexistente")
    return product


def check_favorite_not_exists(client, product_id: str):
    if product_id in client["favorites"]:
        raise HTTPException(status_code=400, detail="Produto ja favoritado")


def check_favorite_exists(client, product_id: str):
    if product_id not in client["favorites"]:
        raise HTTPException(status_code=404, detail="Produto nao esta nos favoritos")


@router.get("/{email}", response_model=FavoritesListOut)  # ALTERE AQUI
def get_favorites(
    email: str,
    request: Request,
    _=Depends(authenticate),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
):
    client = get_client_or_404(email)
    if not client["favorites"]:
        raise HTTPException(
            status_code=404, detail="Nenhum produto favorito foi encontrado"
        )
    favorites = []
    for pid in client["favorites"]:
        product = product_service.get(pid)
        if product:
            favorites.append(product)
    total = len(favorites)
    limit = min(limit, 50)
    start = (page - 1) * limit
    end = start + limit
    page_results = favorites[start:end]
    next_link = None
    if end < total:
        base_url = str(request.url).split("?")[0]
        next_link = f"{base_url}?page={page+1}&limit={limit}"
    return {
        "total": total,
        "page": page,
        "next": next_link,
        "results": page_results,
    }


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
