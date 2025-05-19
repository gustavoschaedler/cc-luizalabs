from fastapi import APIRouter, Depends, HTTPException

from apiluizalabs.auth import get_current_user, oauth2_scheme
from apiluizalabs.schemas import ClientCreate, ClientOut, ClientUpdate
from apiluizalabs.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["Clientes"])

client_service = ClientService()


@router.get("/", response_model=dict)
def list_clients(token: str = Depends(oauth2_scheme)):
    get_current_user(token)
    return client_service.get_all_clients()


@router.get("/{email}", response_model=ClientOut)
def get_client(email: str, token: str = Depends(oauth2_scheme)):
    get_current_user(token)
    client = client_service.get_client(email)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.post("/", response_model=ClientOut, status_code=201)
def create_client(client: ClientCreate, token: str = Depends(oauth2_scheme)):
    get_current_user(token)
    client_data = client.model_dump()
    result = client_service.create_client(client_data)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Converter objetos de produto para IDs de produto
    if "favorites" in result and result["favorites"]:
        result["favorites"] = [prod["id"] for prod in result["favorites"]]

    return result


@router.patch("/{email}", response_model=ClientOut)
def update_client(
    email: str, client: ClientUpdate, token: str = Depends(oauth2_scheme)
):
    get_current_user(token)
    client_data = {k: v for k, v in client.model_dump().items() if v is not None}
    result = client_service.update_client(email, client_data)

    if result is None:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Converter objetos de produto para IDs de produto
    if "favorites" in result and result["favorites"]:
        result["favorites"] = [prod["id"] for prod in result["favorites"]]

    return result


@router.delete("/{email}")
def delete_client(email: str, token: str = Depends(oauth2_scheme)):
    get_current_user(token)
    result = client_service.delete_client(email)
    if not result:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return result
