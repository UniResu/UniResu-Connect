from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import conectar_mongo, fechar_mongo
from routes.usuario_routes import router as router_usuario
from routes.projeto_routes import router as router_projeto # <-- LINHA ADICIONADA

app = FastAPI(title="UniResu API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup_event():
    """Conecta ao banco de dados quando a API inicia."""
    conectar_mongo() 

@app.on_event("shutdown")
async def shutdown_event():
    """Fecha a conexão com o banco quando a API desliga."""
    fechar_mongo() 

@app.get("/")
def home():
    """Rota 'raiz' apenas para verificar se a API está online."""
    return {"status": "Servidor FastAPI rodando!"}

app.include_router(
    router_usuario, 
    prefix="/api",
    tags=["Usuários"] 
)

app.include_router(
    router_projeto, 
    prefix="/api", 
    tags=["Projetos"] 
)