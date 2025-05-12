from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProductFavorite, ProductOut
from app.auth import authenticate
from app.models import clients
from app.services.product_service import get_product

router = APIRouter(prefix="/favorites", tags=["Favoritos"])


@router.post("/{email}")
def add_favorite(email: str, fav: ProductFavorite, _=Depends(authenticate)):
    if email not in clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    product = get_product(fav.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto inexistente")

    if fav.product_id in clients[email]["favorites"]:
        raise HTTPException(status_code=400, detail="Produto ja favoritado")

    clients[email]["favorites"].append(fav.product_id)

    return {"msg": "Produto adicionado aos favoritos com sucesso"}


@router.get("/{email}", response_model=list[ProductOut])
def get_favorites(email: str, _=Depends(authenticate)):
    if email not in clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    favorites = []
    for pid in clients[email]["favorites"]:
        product = get_product(pid)
        if product:
            favorites.append(product)

    return favorites


@router.delete("/{email}/{product_id}")
def remove_favorite(email: str, product_id: str, _=Depends(authenticate)):
    if email not in clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    if product_id not in clients[email]["favorites"]:
        raise HTTPException(status_code=400, detail="Produto nao esta nos favoritos")
    clients[email]["favorites"].remove(product_id)

    return {"msg": "Produto removido dos favoritos com sucesso"}
