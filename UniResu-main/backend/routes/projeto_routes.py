from fastapi import APIRouter, Query, UploadFile, File, Form, HTTPException, Depends
from typing import List, Optional
from controllers.projeto_controller import buscar_projetos_controller
from models.projeto_model import ProjetoResponse, ProjetoCreate
from auth.autenticacao import get_usuario_atual
from database.connection import get_db
from bson import ObjectId
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timezone

router = APIRouter()

@router.get("/projetos/buscar", response_model=List[ProjetoResponse])
async def buscar_projetos_route(
    q: Optional[str] = None,
    local: Optional[str] = None,
    area: Optional[str] = None,
    remoto: bool = False,
    tipos: Optional[str] = Query(None)
):
    return buscar_projetos_controller(q, local, area, remoto, tipos)


@router.post("/projetos/criar", response_model=ProjetoResponse, status_code=201)
def criar_projeto(projeto: ProjetoCreate, usuario_atual=Depends(get_usuario_atual)):
    if usuario_atual.get("vinculo") not in ["professor", "pesquisador"]:
        raise HTTPException(status_code=403, detail="Apenas professores e pesquisadores podem criar projetos.")

    db = get_db()
    novo = projeto.dict()
    novo["data_publicacao"] = datetime.now(timezone.utc).isoformat()
    novo["criado_por"] = usuario_atual["email"]

    resultado = db.projetos.insert_one(novo)
    criado = db.projetos.find_one({"_id": resultado.inserted_id})
    criado["id"] = str(criado["_id"])
    criado["tipo"] = criado.get("tipo_projeto", "")
    criado["dataPublicacao"] = "Publicado recentemente"
    del criado["_id"]
    return criado


@router.delete("/projetos/{projeto_id}")
def excluir_projeto(projeto_id: str, usuario_atual=Depends(get_usuario_atual)):
    if usuario_atual.get("vinculo") not in ["professor", "pesquisador"]:
        raise HTTPException(status_code=403, detail="Acesso negado.")

    db = get_db()
    projeto = db.projetos.find_one({"_id": ObjectId(projeto_id)})

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    if projeto.get("criado_por") != usuario_atual["email"]:
        raise HTTPException(status_code=403, detail="Você só pode excluir seus próprios projetos.")

    db.projetos.delete_one({"_id": ObjectId(projeto_id)})
    return {"mensagem": "Projeto excluído com sucesso."}


@router.put("/projetos/{projeto_id}", response_model=ProjetoResponse)
def editar_projeto(projeto_id: str, projeto: ProjetoCreate, usuario_atual=Depends(get_usuario_atual)):
    if usuario_atual.get("vinculo") not in ["professor", "pesquisador"]:
        raise HTTPException(status_code=403, detail="Acesso negado.")

    db = get_db()
    existente = db.projetos.find_one({"_id": ObjectId(projeto_id)})

    if not existente:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    if existente.get("criado_por") != usuario_atual["email"]:
        raise HTTPException(status_code=403, detail="Você só pode editar seus próprios projetos.")

    db.projetos.update_one({"_id": ObjectId(projeto_id)}, {"$set": projeto.dict()})
    atualizado = db.projetos.find_one({"_id": ObjectId(projeto_id)})
    atualizado["id"] = str(atualizado["_id"])
    atualizado["tipo"] = atualizado.get("tipo_projeto", "")
    atualizado["dataPublicacao"] = "Publicado recentemente"
    del atualizado["_id"]
    return atualizado


@router.post("/projetos/candidatar")
async def candidatar_projeto(
    email_professor: str = Form(...),
    nome_professor: str = Form(...),
    titulo_projeto: str = Form(...),
    nome_aluno: str = Form(...),
    email_aluno: str = Form(...),
    curriculo: UploadFile = File(...)
):
    EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
    EMAIL_SENHA = os.getenv("EMAIL_SENHA_APP")

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = email_professor
        msg["Subject"] = f"Candidatura ao projeto: {titulo_projeto}"

        corpo = f"""
        Olá, {nome_professor}!

        O aluno {nome_aluno} ({email_aluno}) se candidatou ao seu projeto "{titulo_projeto}".

        O currículo está anexado a este email.

        Atenciosamente,
        Plataforma UniResu
        """
        msg.attach(MIMEText(corpo, "plain"))

        conteudo = await curriculo.read()
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(conteudo)
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f'attachment; filename="{curriculo.filename}"')
        msg.attach(parte)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
            servidor.sendmail(EMAIL_REMETENTE, email_professor, msg.as_string())

        return {"mensagem": "Candidatura enviada com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {e}")