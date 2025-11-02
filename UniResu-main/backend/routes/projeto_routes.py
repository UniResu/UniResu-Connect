from fastapi import APIRouter, Query
from typing import List, Optional
from controllers.projeto_controller import buscar_projetos_controller
from models.projeto_model import ProjetoResponse

router = APIRouter()

@router.get(
    "/projetos/buscar", 
    response_model=List[ProjetoResponse]
)
async def buscar_projetos_route(
    q: Optional[str] = None,
    local: Optional[str] = None,
    area: Optional[str] = None,
    remoto: bool = False,
    tipos: Optional[str] = Query(None)
):
    projetos = buscar_projetos_controller(q, local, area, remoto, tipos)
    
    return projetos