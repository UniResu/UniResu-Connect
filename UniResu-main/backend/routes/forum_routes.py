from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from bson import ObjectId
from backend.database.connection import get_db
from backend.auth.autenticacao import get_usuario_atual

router = APIRouter()

class TopicoCriar(BaseModel):
    titulo: str

class VotoInput(BaseModel):
    type: str

def serializar_topico(t: dict) -> dict:
    """Converte o documento MongoDB para um dict serializável."""
    return {
        "id": str(t["_id"]),
        "titulo": t.get("titulo", ""),
        "autor_email": t.get("autor_email", ""),
        "likes": t.get("likes", 0),
        "dislikes": t.get("dislikes", 0),
        "visualizacoes": t.get("visualizacoes", 0),
    }

@router.get("/forum", summary="Listar todos os tópicos (público)")
async def listar_topicos():
    """
    Rota pública — qualquer visitante pode ver os tópicos e seus autores.
    """
    db = get_db()
    topicos = list(db.forum.find())
    return [serializar_topico(t) for t in topicos]


@router.post("/forum", status_code=status.HTTP_201_CREATED, summary="Criar tópico (professor/pesquisador)")
async def criar_topico(
    dados: TopicoCriar,
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """
    Restrição: apenas usuários com vínculo 'professor' ou 'pesquisador' podem criar tópicos.
    """
    vinculos_permitidos = {"professor", "pesquisador"}
    vinculo_usuario = usuario_atual.get("vinculo", "").lower()

    if vinculo_usuario not in vinculos_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas professores e pesquisadores podem criar tópicos."
        )

    titulo = dados.titulo.strip()
    if not titulo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O título do tópico não pode estar vazio."
        )

    novo_topico = {
        "titulo": titulo,
        "autor_email": usuario_atual.get("email", "Desconhecido"),
        "likes": 0,
        "dislikes": 0,
        "visualizacoes": 0,
        "votos_usuarios": {}
    }

    db = get_db()
    resultado = db.forum.insert_one(novo_topico)

    return {
        "mensagem": "Tópico criado com sucesso.",
        "topico": serializar_topico({**novo_topico, "_id": resultado.inserted_id})
    }


@router.delete("/forum/{topico_id}", summary="Deletar tópico (somente o autor)")
async def deletar_topico(
    topico_id: str,
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """
    Restrição: apenas o autor do tópico pode deletá-lo.
    """
    try:
        oid = ObjectId(topico_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de tópico inválido."
        )

    db = get_db()
    topico = db.forum.find_one({"_id": oid})

    if not topico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado."
        )

    if topico.get("autor_email") != usuario_atual.get("email"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este tópico."
        )

    db.forum.delete_one({"_id": oid})

    return {"mensagem": "Tópico deletado com sucesso."}


@router.put("/forum/{topico_id}/votar", summary="Votar em um tópico (autenticado)")
async def votar_topico(
    topico_id: str,
    voto: VotoInput,
    usuario_atual: dict = Depends(get_usuario_atual)
):
    """
    Restrição: apenas usuários logados podem votar.
    - Primeiro voto: computa normalmente.
    - Mesmo botão clicado novamente: desfaz o voto.
    - Botão oposto clicado: troca o voto.
    """
    if voto.type not in ("like", "dislike"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de voto inválido. Use 'like' ou 'dislike'."
        )

    try:
        oid = ObjectId(topico_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de tópico inválido."
        )

    db = get_db()
    topico = db.forum.find_one({"_id": oid})

    if not topico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado."
        )

    email = usuario_atual.get("email")
    votos_usuarios = topico.get("votos_usuarios", {})
    voto_anterior = votos_usuarios.get(email)

    if voto_anterior == voto.type:
        
        update = {
            "$inc": {f"{voto.type}s": -1},
            "$unset": {f"votos_usuarios.{email}": ""}
        }
    elif voto_anterior is None:
        
        update = {
            "$inc": {f"{voto.type}s": 1},
            "$set": {f"votos_usuarios.{email}": voto.type}
        }
    else:
        
        update = {
            "$inc": {f"{voto_anterior}s": -1, f"{voto.type}s": 1},
            "$set": {f"votos_usuarios.{email}": voto.type}
        }

    db.forum.update_one({"_id": oid}, update)
    topico_atualizado = db.forum.find_one({"_id": oid})

    return serializar_topico(topico_atualizado)