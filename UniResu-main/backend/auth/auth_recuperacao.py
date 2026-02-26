import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from backend.database.connection import get_db
from backend.auth.autenticacao import hash_password

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "uniresuconnect@gmail.com"
SMTP_PASS = "" 
URL_FRONTEND = "http://localhost:5500"

router = APIRouter(prefix="/api/auth", tags=["auth"])

tokens_recuperacao: dict = {}

class EsqueciSenhaRequest(BaseModel):
    email: EmailStr

class RedefinirSenhaRequest(BaseModel):
    token: str
    nova_senha: str

def enviar_email(destinatario: str, link: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Redefinição de senha - UniResu"
    msg["From"] = SMTP_USER
    msg["To"] = destinatario

    html = f"""
    <html>
    <body style="font-family: Inter, sans-serif; color: #222; padding: 32px;">
        <h2 style="color: #4c0568;">Redefinição de senha</h2>
        <p>Recebemos uma solicitação para redefinir a senha da sua conta.</p>
        <p>Clique no botão abaixo para criar uma nova senha. O link expira em <strong>1 hora</strong>.</p>
        <a href="{link}" 
        style="display:inline-block; margin-top:16px; padding:12px 24px; 
        background:#7c3aed; color:#fff; border-radius:8px; 
        text-decoration:none; font-weight:600;">
        Redefinir minha senha
        </a>
        <p style="margin-top:24px; color:#888; font-size:13px;">
            Se você não solicitou isso, ignore este e-mail.
        </p>
    </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, destinatario, msg.as_string())

@router.post("/esqueci-senha")
async def esqueci_senha(body: EsqueciSenhaRequest):
    token = secrets.token_urlsafe(32)
    tokens_recuperacao[token] = {
        "email": body.email,
        "expira_em": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    link = f"{URL_FRONTEND}/src/pages/redefinir-senha.html?token={token}"

    try:
        enviar_email(body.email, link)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro ao enviar e-mail: {str(e)}"
        )

    return {"message": "Se o e-mail estiver cadastrado, você receberá o link em breve."}

@router.post("/redefinir-senha")
async def redefinir_senha(body: RedefinirSenhaRequest):
    dados = tokens_recuperacao.get(body.token)

    if not dados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token inválido ou já utilizado."
        )

    if datetime.now(timezone.utc) > dados["expira_em"]:
        tokens_recuperacao.pop(body.token, None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Token expirado. Solicite um novo link."
        )

    if len(body.nova_senha) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="A senha deve ter no mínimo 6 caracteres."
        )

    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro de conexão com o banco de dados."
        )

    email = dados["email"]
    senha_criptografada = hash_password(body.nova_senha)

    resultado = db.usuarios.update_one(
        {"email": email},
        {"$set": {"senha_hash": senha_criptografada}}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado."
        )

    tokens_recuperacao.pop(body.token, None)

    return {"message": "Senha redefinida com sucesso!"}