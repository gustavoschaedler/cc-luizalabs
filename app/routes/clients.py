from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ClientCreate, ClientOut
from app.auth import authenticate
from app.models import clients

router = APIRouter(prefix="/clients", tags=["Clientes"])


@router.post("/", response_model=ClientOut)
def create_client(client: ClientCreate, _=Depends(authenticate)):
    if client.email in clients:
        raise HTTPException(status_code=400, detail="Email ja existe, forneca outro email")

    clients[client.email] = {
        "name": client.name,
        "email": client.email,
        "favorites": [],
    }

    return clients[client.email]


@router.get("/", response_model=list[ClientOut])
def list_clients(_=Depends(authenticate)):
    return list(clients.values())


@router.delete("/{email}")
def delete_client(email: str, _=Depends(authenticate)):
    if email not in clients:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    del clients[email]

    return {"msg": "Cliente removido com sucesso"}
