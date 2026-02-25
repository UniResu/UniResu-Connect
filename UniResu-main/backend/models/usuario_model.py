from pydantic import BaseModel, EmailStr
from pymongo.auth import Optional

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    instituicao: str
    vinculo: str
    orcid_id: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    instituicao: str
    vinculo: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str