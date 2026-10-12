from fastapi import FastAPI
from edocs_ai.api.v1.documents import router as documents_router

from edocs_ai.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="AI Side Intergration for eDcos",
    version=settings.app_version,
)

app.include_router(
    documents_router,
    prefix=settings.api_prefix,
)

@app.get("/")
async def home():
    return {
        "status": "API is working"
    }
@app.get("/health")
async def health():
    return {
        "status": "okay",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }