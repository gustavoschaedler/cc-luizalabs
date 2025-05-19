from fastapi import APIRouter, Depends, HTTPException, Query, Request

from apiluizalabs.auth import get_current_user
from apiluizalabs.models import mem_clients
from apiluizalabs.schemas import ClientCreate, ClientOut, ClientUpdate
from apiluizalabs.services.product_service import get_product_service

product_service = get_product_service()


router = APIRouter(prefix="/clients", tags=["Clientes"])


def validate_favorites_with_errors(favorites):
    if not favorites:
        return [], [], []
    not_found = []
    duplicates = []
    seen = set()
    valid = []
    for prod_id in favorites:
        if prod_id in seen:
            if prod_id not in duplicates:
                duplicates.append(prod_id)
            continue
        exists = product_service.exists(prod_id)
        if not exists:
            not_found.append(prod_id)
        else:
            valid.append(prod_id)
            seen.add(prod_id)
    return valid, not_found, duplicates


def build_client_dict(name, email, favorites):
    return {
        "name": name,
        "email": email,
        "favorites": favorites,
    }


@router.post("/", response_model=ClientOut, status_code=201)
def create_client(client: ClientCreate, _=Depends(get_current_user)):
    if client.email in mem_clients:
        raise HTTPException(
            status_code=400, detail="Email existente, forneca outro email"
        )

    favorites, not_found, duplicates = validate_favorites_with_errors(
        client.favorites or []
    )
    error_msgs = []
    if not_found:
        error_msgs.append(f"Produtos nao encontrado: {', '.join(not_found)}")
    if duplicates:
        error_msgs.append(f"Produtos duplicados: {', '.join(duplicates)}")
    if error_msgs:
        raise HTTPException(status_code=400, detail="; ".join(error_msgs))

    mem_clients[client.email] = build_client_dict(client.name, client.email, favorites)
    return mem_clients[client.email]


@router.get("/")
def list_clients(
    request: Request,
    _=Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
):
    clients = list(mem_clients.values())
    total = len(clients)
    limit = min(limit, 50)
    start = (page - 1) * limit
    end = start + limit
    page_results = clients[start:end]
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


@router.get("/{email}", response_model=ClientOut)
def get_client_by_email(email: str, _=Depends(get_current_user)):
    client = mem_clients.get(email)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return client


@router.delete("/{email}")
def delete_client(email: str, _=Depends(get_current_user)):
    if email not in mem_clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    del mem_clients[email]
    return {"msg": "Cliente removido com sucesso"}


@router.patch("/{email}", response_model=ClientOut)
def update_client(email: str, client_update: ClientUpdate, _=Depends(get_current_user)):
    if email not in mem_clients:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Verifica se o novo email já existe e é diferente do email atual
    if (
        client_update.email
        and client_update.email != email
        and client_update.email in mem_clients
    ):
        raise HTTPException(
            status_code=400, detail="Email existente, forneca outro email"
        )

    # Atualiza os campos do cliente
    client_dict = mem_clients[email]

    # Atualiza o nome se fornecido
    if client_update.name:
        client_dict["name"] = client_update.name

    # Atualiza os favoritos se fornecidos
    if client_update.favorites is not None:
        favorites, not_found, duplicates = validate_favorites_with_errors(
            client_update.favorites
        )
        error_msgs = []
        if not_found:
            error_msgs.append(f"Produtos nao encontrado: {', '.join(not_found)}")
        if duplicates:
            error_msgs.append(f"Produtos duplicados: {', '.join(duplicates)}")
        if error_msgs:
            raise HTTPException(status_code=400, detail="; ".join(error_msgs))
        client_dict["favorites"] = favorites

    # Atualiza o email se fornecido (e já validado acima)
    if client_update.email and client_update.email != email:
        # Atualiza o campo email dentro do dicionário do cliente
        client_dict["email"] = client_update.email
        # Move o cliente para a nova chave no dicionário mem_clients
        mem_clients[client_update.email] = client_dict
        del mem_clients[email]

    return client_dict
