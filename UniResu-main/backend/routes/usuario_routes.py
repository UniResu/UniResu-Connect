from fastapi import APIRouter, HTTPException, status
from typing import List
from backend.database.connection import get_db
from backend.models.usuario_model import UsuarioCreate, UsuarioResponse, UsuarioLogin
from backend.auth.autenticacao import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def formatar_usuario(usuario_db):
    return {
        "id": str(usuario_db["_id"]),
        "nome": usuario_db.get("nome", "Usuário sem nome"),
        "email": usuario_db.get("email", ""),
        "instituicao": usuario_db.get("instituicao", ""),
        "vinculo": usuario_db.get("vinculo", "")
    }

@router.get("", response_model=List[UsuarioResponse])
def listar_usuarios():
    """Retorna a lista de todos os usuários (resolvendo o 404 do frontend)"""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB não conectado")
    
    usuarios_cursor = db.usuarios.find()
    return [formatar_usuario(u) for u in usuarios_cursor]

@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(user: UsuarioCreate):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

    if db.usuarios.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Este email já está cadastrado.")

    novo_usuario = {
        "nome": user.nome,
        "email": user.email,
        "senha_hash": hash_password(user.senha),
        "instituicao": user.instituicao,
        "vinculo": user.vinculo
    }

    try:
        resultado = db.usuarios.insert_one(novo_usuario)
        usuario_criado = db.usuarios.find_one({"_id": resultado.inserted_id})
        return formatar_usuario(usuario_criado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")

@router.post("/login")
def login_usuario(user: UsuarioLogin):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    usuario_db = db.usuarios.find_one({"email": user.email})
    
    if not usuario_db or not verify_password(user.senha, usuario_db.get("senha_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )
        
    token = create_access_token(data={"sub": usuario_db["email"]})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "nome": usuario_db.get("nome", "Usuário sem nome"),
        "email": usuario_db.get("email", ""), 
        "vinculo": usuario_db.get("vinculo", "Não informado")
    }