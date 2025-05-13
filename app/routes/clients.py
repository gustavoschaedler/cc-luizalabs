import os

import requests
from fastapi import APIRouter, Depends, HTTPException

from app.auth import authenticate
from app.models import mem_clients
from app.schemas import ClientCreate, ClientOut, ClientUpdate
from app.services.product_service import get_product_service

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
def create_client(client: ClientCreate, _=Depends(authenticate)):
    if client.email in mem_clients:
        raise HTTPException(
            status_code=400, detail="Email ja existe, forneca outro email"
        )

    favorites, not_found, duplicates = validate_favorites_with_errors(
        client.favorites or []
    )
    error_msgs = []
    if not_found:
        error_msgs.append(f"Produtos inexistentes: {', '.join(not_found)}")
    if duplicates:
        error_msgs.append(f"Produtos duplicados: {', '.join(duplicates)}")
    if error_msgs:
        raise HTTPException(status_code=400, detail="; ".join(error_msgs))

    mem_clients[client.email] = build_client_dict(client.name, client.email, favorites)
    return mem_clients[client.email]


@router.get("/", response_model=list[ClientOut])
def list_clients(_=Depends(authenticate)):
    return list(mem_clients.values())


@router.get("/{email}", response_model=ClientOut)
def get_client_by_email(email: str, _=Depends(authenticate)):
    client = mem_clients.get(email)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return client


@router.delete("/{email}")
def delete_client(email: str, _=Depends(authenticate)):
    if email not in mem_clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    del mem_clients[email]
    return {"msg": "Cliente removido com sucesso"}


@router.patch("/{email}", response_model=ClientOut)
def update_client(email: str, client_update: ClientUpdate, _=Depends(authenticate)):
    if email not in mem_clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    client_data = mem_clients[email]

    if client_update.name is not None:
        client_data["name"] = client_update.name

    if client_update.email is not None:
        mem_clients[client_update.email] = mem_clients.pop(email)
        mem_clients[client_update.email]["email"] = client_update.email
        email = client_update.email
        client_data = mem_clients[email]

    if client_update.favorites is not None:
        favorites, not_found, duplicates = validate_favorites_with_errors(
            client_update.favorites
        )
        error_msgs = []
        if not_found:
            error_msgs.append(f"Produtos inexistentes: {', '.join(not_found)}")
        if duplicates:
            error_msgs.append(f"Produtos duplicados: {', '.join(duplicates)}")
        if error_msgs:
            raise HTTPException(status_code=400, detail="; ".join(error_msgs))
        client_data["favorites"] = favorites

    return client_data
