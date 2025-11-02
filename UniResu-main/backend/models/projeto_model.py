from pydantic import BaseModel, Field
from typing import Optional
class ProjetoResponse(BaseModel):
    id: str

    titulo: str
    descricao: str
    instituicao: Optional[str]
    tipo: Optional[str]
    dataPublicacao: Optional[str]

    local: Optional[str]
    area_estudo: Optional[str] 
    e_remoto: Optional[bool]

    class Config:
        populate_by_name = True 
        from_attributes = True  