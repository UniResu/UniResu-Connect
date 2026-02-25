from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.connection import conectar_mongo, fechar_mongo
from backend.routes.usuario_routes import router as router_usuario
from backend.routes.projeto_routes import router as router_projeto
from backend.routes.forum_routes import router as router_forum
from backend.auth.auth_recuperacao import router as recuperacao_router
from backend.routes.orcid_routes import router as router_orcid
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="UniResu API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    conectar_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    fechar_mongo()

@app.get("/")
def home():
    return {"status": "Servidor FastAPI rodando!"}

app.include_router(router_usuario, prefix="/api", tags=["Usuários"])
app.include_router(router_projeto, prefix="/api", tags=["Projetos"])
app.include_router(router_forum, prefix="/api", tags=["Fórum"])
app.include_router(recuperacao_router)
app.include_router(router_orcid)