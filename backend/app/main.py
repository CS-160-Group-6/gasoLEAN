from fastapi import FastAPI
import uvicorn

from app.config import settings
from app.db.session import engine
from app.db.models import Base
from app.api.v1.routers.health import router as health_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="gasoLEAN API",
    version="0.0.1",
    openapi_url="/openapi.json"
)

app.include_router(
    router=health_router,
    prefix="/api/v1",
    tags=["health"]
)

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )