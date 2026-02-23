from typing import List, Optional, Dict, Any
from database.connection import get_db

TIPO_LABELS = {
    "institucional_aberto": "Projeto Institucional (Aberto)",
    "institucional_exclusivo": "Projeto Institucional (Exclusivo)",
    "voluntario_aberto": "Projeto Voluntário (Aberto)",
    "voluntario_exclusivo": "Projeto Voluntário (Exclusivo)",
}

def formatar_projeto(doc: Dict[str, Any]) -> Dict[str, Any]:
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]

    if "tipo_projeto" in doc:
        doc["tipo"] = TIPO_LABELS.get(doc["tipo_projeto"], doc["tipo_projeto"])

    if "data_publicacao" in doc:
        doc["dataPublicacao"] = "Publicado recentemente"

    return doc

def buscar_projetos_controller(
    q: Optional[str],
    local: Optional[str],
    area: Optional[str],
    remoto: bool,
    tipos: Optional[str]
) -> List[Dict[str, Any]]:

    db = get_db()
    if db is None:
        return []

    query_filter = {}

    if q:
        query_filter["$or"] = [
            {"titulo": {"$regex": q, "$options": "i"}},
            {"descricao": {"$regex": q, "$options": "i"}}
        ]
    if local:
        query_filter["local"] = {"$regex": local, "$options": "i"}
    if area:
        query_filter["area_estudo"] = area
    if remoto:
        query_filter["e_remoto"] = True
    if tipos:
        if lista_de_tipos := tipos.split(','):
            query_filter["tipo_projeto"] = {"$in": lista_de_tipos}

    try:
        cursor = db.projetos.find(query_filter)
        return [formatar_projeto(doc) for doc in cursor.limit(50)]
    except Exception as e:
        print(f"❌ Erro na consulta ao MongoDB: {e}")
        return []