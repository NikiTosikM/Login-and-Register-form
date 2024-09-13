from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from auth.router import router


import logging


logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(router, prefix="/auth", tags=["auth"])

@app.exception_handler(OSError)
async def connect_db(request: Request, exc:OSError):
    logger.error('Произошла ошибка с базой данных')
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail":  "Database connection error",
                "error_name": str(exc)    
        }
    )

