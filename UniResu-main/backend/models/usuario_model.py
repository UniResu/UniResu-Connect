from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioCreate(BaseModel):
    email: EmailStr  
    senha: str
class UsuarioResponse(BaseModel):
    id: str
    email: EmailStr

    class Config:
        from_attributes = True 
        from_attributes = True