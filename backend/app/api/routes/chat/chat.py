from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from app.db.engine import get_session
from sqlalchemy.orm import Session
from app.services.auth.users import current_user
from app.db.models import User
from app.services.ingestion import ingestion
from app.api.routes.chat.models import ChatQuery
from app.services.chat.chat import query_handling

router = APIRouter(prefix="/manage", tags=["file upload"])


@router.post("/chat")
def upload_file(
    _: User | None = Depends(current_user),
    db_session: Session = Depends(get_session),
    chat_query: ChatQuery = ChatQuery,
):
    try:
        return query_handling(chat_query=chat_query)
    except Exception as e:
        HTTPException(
            status_code=404,
            detail=f"Something went wrong while generating res :{str(e)}",
        )
