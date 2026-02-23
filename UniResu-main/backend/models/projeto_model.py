from pydantic import BaseModel
from typing import Optional

class ProjetoCreate(BaseModel):
    titulo: str
    descricao: str
    instituicao: str
    local: Optional[str]
    area_estudo: str
    tipo_projeto: str
    e_remoto: bool = False
    nome_professor: str
    email_professor: str

class ProjetoResponse(BaseModel):
    id: str
    titulo: str
    descricao: str
    instituicao: Optional[str]
    tipo: Optional[str]
    tipo_projeto: Optional[str]
    dataPublicacao: Optional[str]
    local: Optional[str]
    area_estudo: Optional[str]
    e_remoto: Optional[bool]
    nome_professor: Optional[str]
    email_professor: Optional[str]

    class Config:
        populate_by_name = True
        from_attributes = True