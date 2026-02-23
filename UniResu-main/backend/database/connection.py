import os
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / ".env"

if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"⚠️ AVISO: Arquivo .env não encontrado em: {dotenv_path}")

MONGO_URI = os.getenv("MONGO_URI")

client: MongoClient = None
db = None

def conectar_mongo():
    """
    Inicializa a conexão com o MongoDB Atlas.
    """
    global client, db
    try:
        if not MONGO_URI:
            raise ValueError(f"Variável MONGO_URI não definida. Verifique seu .env em {dotenv_path}")

        client = MongoClient(MONGO_URI)

        client.admin.command('ping')

        db = client["UniResuDB"] 
        print(f"✅ Conectado ao MongoDB Atlas (Banco: {db.name})")

    except Exception as e:
        print(f"❌ Erro crítico ao conectar ao MongoDB: {e}")
        db = None
        client = None

def fechar_mongo():
    """
    Fecha a conexão de forma limpa. Chamado no shutdown do FastAPI.
    """
    global client
    if client:
        client.close()
        print("🔌 Conexão com MongoDB fechada.")

def get_db():
    """
    Retorna a instância do banco de dados para os controllers.
    """
    global db
    return db