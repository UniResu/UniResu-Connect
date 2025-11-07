from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

MONGO_URI = os.getenv("MONGO_URI")

client: MongoClient = None
db = None

def conectar_mongo():
    global client, db
    try:
        if not MONGO_URI:
            print("❌ ERRO: Variável MONGO_URI não encontrada.")
            print("   Verifique se seu arquivo .env está em UniResu-main/ e não em backend/")
            return

        client = MongoClient(MONGO_URI)
        db = client["UniResuDB"] 
        print(f"✅ Conectado ao MongoDB Atlas (Banco: {db.name})")

    except Exception as e:
        print(f"❌ Erro ao conectar ao MongoDB: {e}")

def fechar_mongo():
    """
    Esta função é chamada pelo 'shutdown' do FastAPI.
    """
    global client
    if client:
        client.close()
        print("🔌 Conexão com MongoDB fechada.")

def get_db():
    """
    Esta é a função que suas rotas (routes) vão usar
    para acessar o banco de dados.
    """
    return db