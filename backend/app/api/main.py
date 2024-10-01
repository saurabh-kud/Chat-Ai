from fastapi import APIRouter
from app.api.routes import users
from app.api.routes import auth


api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth.router)
