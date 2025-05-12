from fastapi import APIRouter, HTTPException
from app.schemas import ProductOut
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Produtos (Mock)"])

@router.get("/", response_model=list[ProductOut])
def list_products():
    produtos = product_service.get_all_products()
    if produtos is None:
        raise HTTPException(status_code=502, detail="Erro ao acessar produtos")
    return produtos

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str):
    produto = product_service.get_product(product_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/mock/{total}", response_model=list[ProductOut], status_code=201)
def create_mock_products(total: int):
    try:
        produtos = product_service.create_mock_products(total)
        return produtos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
