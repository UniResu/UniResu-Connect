from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    instituicao: str
    vinculo: str

class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    instituicao: str
    vinculo: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str