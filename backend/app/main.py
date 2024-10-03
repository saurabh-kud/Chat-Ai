from fastapi import FastAPI, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uvicorn


startTime = time.time()
from app.config import APP_NAME
from app.config import APP_HOST
from app.config import PYTHON_ENV
from app.config import APP_VERSION
from app.config import DOCS_ENABLED
from app.utils import custom_handler
from app.utils.uptime import getUptime

from app.api.main import api_router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="advanced chatbot for your files",
    docs_url="/api/docs" if DOCS_ENABLED else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(custom_handler.CustomException)
async def handle_custom_exception(request, exc: custom_handler.CustomException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.msg})


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Route"])
async def health_route(req: Request):
    """
    Health Route : Returns App details.
    """
    return JSONResponse(
        {
            "app": APP_NAME,
            "version": "v" + APP_VERSION,
            "ip": req.client.host,
            "uptime": getUptime(startTime),
            # "database": "connected" if is_db_connected() else "disconnected",
            "mode": PYTHON_ENV,
        }
    )


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
