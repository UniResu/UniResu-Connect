from fastapi import APIRouter, Query, UploadFile, File, Form, HTTPException
from typing import List, Optional
from controllers.projeto_controller import buscar_projetos_controller
from models.projeto_model import ProjetoResponse
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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
    
    print(f"EMAIL: {EMAIL_REMETENTE}")
    print(f"SENHA: {EMAIL_SENHA}")

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

        conteudo_curriculo = await curriculo.read()
        parte = MIMEBase("application", "octet-stream")
        parte.set_payload(conteudo_curriculo)
        encoders.encode_base64(parte)
        parte.add_header("Content-Disposition", f'attachment; filename="{curriculo.filename}"')
        msg.attach(parte)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
            servidor.sendmail(EMAIL_REMETENTE, email_professor, msg.as_string())

        return {"mensagem": "Candidatura enviada com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar email: {e}")