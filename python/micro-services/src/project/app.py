# Standard Library
import logging

# Third Party Library
from fastapi import FastAPI, Request
from starlette import status
from starlette.responses import JSONResponse

# Project Library
from project.configs import project_config
from project.core.utils.log import setup_logger_format
# from project.routers.emails import router as emails_router

# from starlette.middleware.cors import CORSMiddleware


config = project_config.AppConfig()
config.load_config()

logger = logging.getLogger(__name__)

setup_logger_format(logger)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": "internal server error", "status": False, "error": str(e)}
        )


@app.get("/api/v1/project/health-check")
def health_check():
    logger.info("Health check API is working")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": True,
            "data": None,
            "message": "project Service is working . . .",
        },
    )


# app.include_router(emails_router, tags=["Emails processing"], prefix="/api/v1/email")
