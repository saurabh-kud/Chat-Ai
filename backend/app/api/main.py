from fastapi import APIRouter
from app.api.routes.users import users
from app.api.routes.auth import auth
from app.api.routes.ingestion import ingestion
from app.api.routes.chat import chat


api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(ingestion.router)
api_router.include_router(chat.router)
