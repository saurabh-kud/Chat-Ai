import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "password"
POSTGRES_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
POSTGRES_PORT = os.environ.get("POSTGRES_PORT") or "5432"
POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"


APP_NAME = os.environ.get("APP_NAME") or "chat-ai"
APP_VERSION = os.environ.get("APP_VERSION") or "0.0.1"
APP_HOST = os.environ.get("POSTGRES_DB") or "0.0.0.0"
PORT = os.environ.get("POSTGRES_DB") or "8080"
PYTHON_ENV = os.environ.get("PYTHON_ENV") or "development"
DOCS_ENABLED = os.environ.get("DOCS_ENABLED") or True
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") or None
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or None
QDRANT_HOST = os.environ.get("QDRANT_HOST") or "chatai-stack-index-1"
QDRANT_PORT = os.environ.get("QDRANT_PORT") or 6333
