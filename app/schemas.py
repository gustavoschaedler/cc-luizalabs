from pydantic import BaseModel, EmailStr
from typing import List, Optional


class ClientCreate(BaseModel):
    name: str
    email: EmailStr


class ClientOut(ClientCreate):
    favorites: List[str] = []


class ProductFavorite(BaseModel):
    product_id: str


class ProductCreate(BaseModel):
    title: str
    image: str
    price: float
    brand: str
    reviewScore: Optional[float] = None


class ProductOut(BaseModel):
    id: str
    title: str
    image: str
    price: float
    brand: str
    reviewScore: Optional[float] = None

