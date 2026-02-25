import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from backend.database.connection import get_db

load_dotenv(dotenv_path="../.env")

SECRET_KEY = os.getenv("SECRET_KEY", "a45a306135f631b0179a618f0a8274d119436f010b93a0c36b8018f3b1ac6c7a")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/usuarios/login")

def hash_password(password: str):
    """Criptografa a senha antes de salvar no banco."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """Compara a senha digitada com a senha do banco."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Gera o token de login JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    """
    Decodifica o token JWT e retorna os dados do usuário.
    Esta função protege rotas que exigem login (como as do fórum).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB não conectado")

    usuario = db.usuarios.find_one({"email": email})

    if usuario is None:
        raise credentials_exception

    usuario["id"] = str(usuario["_id"])
    if "senha_hash" in usuario:
        del usuario["senha_hash"]
    del usuario["_id"]

    return usuario