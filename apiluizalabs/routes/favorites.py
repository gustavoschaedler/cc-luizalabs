from fastapi import APIRouter, Depends, HTTPException

from apiluizalabs.auth import get_current_user, oauth2_scheme
from apiluizalabs.schemas import FavoritesListOut, ProductFavorite
from apiluizalabs.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["Favoritos"])

favorite_service = FavoriteService()


@router.get("/{email}", response_model=FavoritesListOut)
def list_favorites(email: str, token: str = Depends(oauth2_scheme)):
    get_current_user(token)
    favorites = favorite_service.get_favorites(email)
    if favorites is None:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return {"favorites": favorites}


@router.post("/{email}", response_model=FavoritesListOut)
def add_favorite(
    email: str, product: ProductFavorite, token: str = Depends(oauth2_scheme)
):
    get_current_user(token)
    result = favorite_service.add_favorite(email, product.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Cliente ou produto nao encontrado")
    return {"favorites": result}


@router.delete("/{email}/{product_id}", response_model=FavoritesListOut)
def remove_favorite(email: str, product_id: str, token: str = Depends(oauth2_scheme)):
    get_current_user(token)
    result = favorite_service.remove_favorite(email, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Produto nao esta nos favoritos")
    return {"favorites": result}
