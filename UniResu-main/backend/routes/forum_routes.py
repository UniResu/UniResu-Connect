from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from pymongo.results import InsertOneResult, UpdateResult
from bson import ObjectId
from database.connection import get_db
from models.forum_model import TopicoCreate, TopicoResponse, RespostaCreate
from auth.autenticacao import get_usuario_atual

router = APIRouter()

def formatar_topico(doc: Dict[str, Any]) -> Dict[str, Any]:
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc

@router.get(
    "/forum/topicos",
    response_model=List[TopicoResponse]
)
def listar_topicos():
    """
    Lista todos os tópicos do fórum (como na sua imagem).
    Esta rota é pública.
    """
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="DB não conectado")

    try:
        lista_docs = list(db.topicos_forum.find({}))
        return [formatar_topico(doc) for doc in lista_docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {e}")

@router.post(
    "/forum/topicos",
    response_model=TopicoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_topico(
    topico: TopicoCreate, 
    usuario_logado: dict = Depends(get_usuario_atual) 
):
    """
    Cria um novo tópico no fórum.
    Requer que o usuário esteja autenticado.
    """
    db = get_db()
    
    novo_topico_doc = {
        "titulo": topico.titulo,
        "conteudo_original": topico.conteudo,
        "autor_email": usuario_logado["email"], 
        "data_criacao": datetime.now(timezone.utc),
        "visualizacoes": 0,
        "respostas": [] 
    }
    
    try:
        inserted: InsertOneResult = db.topicos_forum.insert_one(novo_topico_doc)
        topico_criado = db.topicos_forum.find_one({"_id": inserted.inserted_id})
        
        if not topico_criado:
            raise HTTPException(status_code=500, detail="Erro ao criar tópico")

        return formatar_topico(topico_criado)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {e}")

@router.post(
    "/forum/topicos/{topico_id}/responder",
    response_model=TopicoResponse
)
def adicionar_resposta(
    topico_id: str,
    resposta: RespostaCreate,
    usuario_logado: dict = Depends(get_usuario_atual)
):
    """
    Adiciona uma resposta (dúvida) a um tópico existente.
    Requer que o usuário esteja autenticado.
    """
    db = get_db()
    
    nova_resposta_doc = {
        "_id": ObjectId(),
        "conteudo": resposta.conteudo,
        "autor_email": usuario_logado["email"],
        "data_postagem": datetime.now(timezone.utc)
    }
    
    try:
        update_result: UpdateResult = db.topicos_forum.update_one(
            {"_id": ObjectId(topico_id)}, 
            {"$push": {"respostas": nova_resposta_doc}}
        )
        
        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Tópico não encontrado")
            
        topico_atualizado = db.topicos_forum.find_one({"_id": ObjectId(topico_id)})
        return formatar_topico(topico_atualizado)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {e}")