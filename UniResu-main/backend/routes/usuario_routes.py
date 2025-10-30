from fastapi import APIRouter
from database.connection import get_db 

router = APIRouter()

@router.get("/usuarios")
def get_usuarios():
    db = get_db() 
    
    if db is None:
        return {"erro": "Banco de dados não conectado"}, 500

    try:
        lista_usuarios = list(db["usuarios"].find({}, {"_id": 0})) 
        return {"usuarios": lista_usuarios}
    
    except Exception as e:
        return {"erro": f"Erro ao buscar usuários: {str(e)}"}, 500
