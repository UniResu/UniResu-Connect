from pydantic import BaseModel
from typing import Optional

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