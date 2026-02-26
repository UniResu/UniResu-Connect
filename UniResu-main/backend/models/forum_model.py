from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional
from datetime import datetime

class RespostaCreate(BaseModel):
    """Modelo para o que o usuário envia ao responder."""
    descricao: str


class RespostaInDB(BaseModel):
    """Modelo de como a resposta é salva no banco."""
    id: str = Field(alias="_id")
    descricao: str
    autor_email: str
    data_postagem: datetime = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        from_attributes = True


class TopicoCreate(BaseModel):
    """Modelo para o que o usuário envia ao criar um tópico."""
    titulo: str
    descricao: str = ""

    @field_validator("titulo")
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("O título não pode estar vazio.")
        return v.strip()

    @field_validator("descricao")
    @classmethod
    def descricao_nao_vazia(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("A descrição não pode estar vazia.")
        return v.strip()


class VotoCreate(BaseModel):
    """Modelo para o payload de votação enviado pelo frontend."""
    type: str

    @field_validator("type")
    @classmethod
    def type_valido(cls, v: str) -> str:
        if v in {"like", "dislike"}:
            return v
        raise ValueError("Tipo de voto inválido. Use 'like' ou 'dislike'.")


class TopicoResponse(BaseModel):
    """Modelo para o que a API retorna ao listar tópicos."""
    id: str = Field(alias="_id")
    titulo: str
    descricao: str = ""  
    autor_email: str
    data_criacao: datetime
    visualizacoes: int = 0
    likes: int = 0
    dislikes: int = 0
    respostas: List[RespostaInDB] = []

    votos_usuarios: Dict[str, str] = Field(default_factory=dict)
    user_liked: bool = False
    user_disliked: bool = False

    class Config:
        populate_by_name = True
        from_attributes = True