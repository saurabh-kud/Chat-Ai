from fastapi import APIRouter
from app.api.routes import users
from app.api.routes import auth
from app.api.routes.ingestion import ingestion


api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(ingestion.router)
