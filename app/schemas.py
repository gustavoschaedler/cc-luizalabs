from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum

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

class BrandEnum(str, Enum):
    NIKE = "Nike"
    ADIDAS = "Adidas"
    PUMA = "Puma"
    REEBOK = "Reebok"
    FILA = "Fila"
    MIZUNO = "Mizuno"

