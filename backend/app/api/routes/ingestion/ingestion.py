from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile, File
from app.db.engine import get_session
from sqlalchemy.orm import Session
from app.services.auth.users import current_user
from app.db.models import User
from app.services.ingestion import ingestion
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/manage", tags=["file upload"])


@router.post("/file")
def upload_file(
    _: User | None = Depends(current_user),
    db_session: Session = Depends(get_session),
    file: UploadFile = File(...),
):
    try:
        if not file:
            raise HTTPException(status_code=404, detail="no file provided")
        if not file.filename:
            raise HTTPException(status_code=400, detail="file name not available")

        file_path = ingestion.file_processing(file=file)

        return JSONResponse(
            content={
                "message": "File uploaded successfully",
                "file_path": str(file_path),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
