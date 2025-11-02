from pymongo.results import InsertOneResult
from typing import Dict, Any
from fastapi import HTTPException, status
from passlib.context import CryptContext
from database.connection import get_db
from models.usuario_model import UsuarioCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha pura bate com o hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)

def formatar_usuario(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converte o _id para id."""
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

def registrar_usuario_controller(user: UsuarioCreate) -> Dict[str, Any]:
    """
    Controlador para registrar um novo usuário.
    """
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Não foi possível conectar ao banco de dados."
        )

    usuario_existente = db.usuarios.find_one({"email": user.email})
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este email já está cadastrado."
        )

    senha_hash = hash_password(user.senha)

    novo_usuario_doc = {
        "email": user.email,
        "senha_hash": senha_hash
    }

    try:
        inserted: InsertOneResult = db.usuarios.insert_one(novo_usuario_doc)

        usuario_criado = db.usuarios.find_one({"_id": inserted.inserted_id})
        
        if usuario_criado is None:
             raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Erro ao criar o usuário."
            )

        return formatar_usuario(usuario_criado)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro interno do servidor: {e}"
        )