import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from database.connection import get_db

load_dotenv(dotenv_path="../.env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY não configurada")

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    """
    Decodifica o token JWT e retorna os dados do usuário.
    Esta é a função que vai "proteger" nossas rotas.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not SECRET_KEY:
        raise HTTPException(status_code=500, detail="SECRET_KEY não configurada")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB não conectado")

    usuario = db.usuarios.find_one({"email": email})

    if usuario is None:
        raise credentials_exception

    usuario["id"] = str(usuario["_id"])
    del usuario["senha_hash"]
    del usuario["_id"]

    return usuario