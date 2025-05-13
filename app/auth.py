import secrets

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    # TODO: Implementar autenticação real (JWT, OAuth, etc.)
    correct_user = secrets.compare_digest(credentials.username, "admin")
    correct_pass = secrets.compare_digest(credentials.password, "admin123")

    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return credentials.username
