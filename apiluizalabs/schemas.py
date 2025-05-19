from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    name: str
    email: EmailStr


class ClientCreate(ClientBase):
    favorites: Optional[List[str]] = None


class ClientOut(ClientBase):
    favorites: List[str]


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    favorites: Optional[List[str]] = None


class ProductFavorite(BaseModel):
    id: str


class ProductOut(BaseModel):
    id: str
    title: str
    price: float
    image: str
    brand: str
    reviewScore: Optional[float] = None


class FavoritesListOut(BaseModel):
    favorites: List[ProductOut]


class BrandEnum(str, Enum):
    NIKE = "Nike"
    ADIDAS = "Adidas"
    PUMA = "Puma"
    REEBOK = "Reebok"
    FILA = "Fila"
    MIZUNO = "Mizuno"


class FavoriteAdd(BaseModel):
    id: str


class FavoriteList(BaseModel):
    total: int
    page: int
    next: Optional[str] = None
    results: List = []
    favorites: List[str] = []
