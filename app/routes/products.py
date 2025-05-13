from fastapi import APIRouter, HTTPException

from app.schemas import ProductOut
from app.services.product_service import get_product_service

router = APIRouter(prefix="/products", tags=["Produtos (Mock)"])

product_service = get_product_service()


@router.get("/", response_model=list[ProductOut])
def list_products():
    produtos = product_service.get_all()
    if produtos is None:
        raise HTTPException(status_code=502, detail="Erro ao acessar produtos")
    return produtos


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str):
    produto = product_service.get(product_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao existe")
    return produto


@router.post("/mock/{total}", response_model=list[ProductOut], status_code=201)
def create_mock_products(total: int):
    try:
        if not hasattr(product_service, "create_mock_products"):
            raise HTTPException(
                status_code=400, detail="Operacaoo nao suportada para API externa"
            )
        produtos = product_service.create_mock_products(total)
        return produtos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
