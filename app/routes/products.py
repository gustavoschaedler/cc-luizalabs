from fastapi import APIRouter, Depends, HTTPException, Query, Request, Security

from app.auth import get_current_user, oauth2_scheme
from app.schemas import ProductOut
from app.services.product_service import get_product_service

router = APIRouter(prefix="/products", tags=["Produtos (Mock)"])

product_service = get_product_service()


@router.get("/")
def list_products(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    token: str = Depends(oauth2_scheme),
):
    user = get_current_user(token)
    produtos = product_service.get_all()
    if produtos is None:
        raise HTTPException(status_code=502, detail="Erro ao acessar produtos")
    total = len(produtos)
    limit = min(limit, 50)
    start = (page - 1) * limit
    end = start + limit
    page_results = produtos[start:end]
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


@router.get("/{id}", response_model=ProductOut)
def get_product(id: str, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    produto = product_service.get(id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao existe")
    return produto


@router.post("/mock/{total}", response_model=list[ProductOut], status_code=201)
def create_mock_products(total: int, token: str = Depends(oauth2_scheme)):
    user = get_current_user(token)
    try:
        if not hasattr(product_service, "create_mock_products"):
            raise HTTPException(
                status_code=400, detail="Operacaoo nao suportada para API externa"
            )
        produtos = product_service.create_mock_products(total)
        return produtos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
