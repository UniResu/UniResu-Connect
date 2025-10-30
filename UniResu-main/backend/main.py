from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import conectar_mongo, fechar_mongo
from routes.usuario_routes import router as router_usuario

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
    conectar_mongo() 

@app.on_event("shutdown")
async def shutdown_event():
    fechar_mongo() 

@app.get("/")
def home():
    return {"status": "Servidor FastAPI rodando!"}

app.include_router(
    router_usuario, 
    prefix="/api",
    tags=["Usuários"] 
)