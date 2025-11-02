from fastapi import APIRouter, HTTPException, status
from database.connection import get_db 
from typing import List, Dict, Any
from pymongo.results import InsertOneResult
import bcrypt 
from models.usuario_model import UsuarioCreate, UsuarioResponse

router = APIRouter()

def hash_password(password: str) -> str:
    """Gera o hash de uma senha usando bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha pura bate com o hash salvo."""
    try:
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except Exception:
        return False

def formatar_usuario(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converte o _id (ObjectId) do MongoDB para uma string 'id'."""
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

@router.get(
    "/usuarios", 
    response_model=List[UsuarioResponse]
)
def get_usuarios():
    db = get_db() 
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Banco de dados não conectado"
        )
    try:
        lista_docs = list(db["usuarios"].find({}))
        return [formatar_usuario(doc) for doc in lista_docs]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro ao buscar usuários: {str(e)}"
        )

@router.post(
    "/usuarios/registrar", 
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario_route(user: UsuarioCreate):
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Banco de dados não conectado"
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
        print("\n\n!!!!!!!!!! OCORREU UM ERRO INTERNO !!!!!!!!!!")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro interno: {e}"
        )