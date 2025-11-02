from typing import List, Optional, Dict, Any
from database.connection import get_db 

def formatar_projeto(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Converte _id para id e ajusta nomes de campos para o JS."""
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]

    if "tipo_projeto" in doc:
        if doc["tipo_projeto"] == "institucional_exclusivo":
            doc["tipo"] = "Projeto Institucional (Exclusivo)"
        elif doc["tipo_projeto"] == "voluntario_aberto":
            doc["tipo"] = "Projeto Voluntário (Aberto)"
        else:
            doc["tipo"] = doc["tipo_projeto"]
            
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
        print("❌ ERRO no Controller: Não foi possível obter o 'db'.")
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
        lista_de_tipos = tipos.split(',')
        if lista_de_tipos:
            query_filter["tipo_projeto"] = {"$in": lista_de_tipos}

    try:
        cursor = db.projetos.find(query_filter)
        resultados = list(cursor.limit(50))
        
        resultados_formatados = [formatar_projeto(doc) for doc in resultados]
        return resultados_formatados

    except Exception as e:
        print(f"❌ Erro na consulta ao MongoDB: {e}")
        return []