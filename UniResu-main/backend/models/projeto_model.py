from pydantic import BaseModel
from typing import Optional

class ProjetoCreate(BaseModel):
    titulo: str
    descricao: str
    instituicao: str
    local: Optional[str]
    area_estudo: str
    tipo_projeto: str
    modalidade: str
    nome_professor: str
    email_professor: str

class ProjetoResponse(BaseModel):
    id: str
    titulo: str
    descricao: str
    instituicao: Optional[str] = None
    tipo: Optional[str] = None
    tipo_projeto: Optional[str] = None
    dataPublicacao: Optional[str] = None
    local: Optional[str] = None
    area_estudo: Optional[str] = None
    e_remoto: Optional[bool] = None
    modalidade: Optional[str] = None
    nome_professor: Optional[str] = None
    email_professor: Optional[str] = None
    class Config:
        populate_by_name = True
        from_attributes = True