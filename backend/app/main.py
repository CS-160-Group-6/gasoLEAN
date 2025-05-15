import os
import sys

# Add the parent directory to the Python path
HERE: str = os.path.dirname(os.path.abspath(path=__file__))
PARENT_DIR: str = os.path.dirname(HERE)

if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import settings
from app.db.session import engine
from app.db.models import Base
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.rides import router as rides_router
from app.api.v1.routers.measurement_stream import router as measurement_stream_router
from app.api.v1.routers import profiles
from app.api.v1.routers import vehicle

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="gasoLEAN API",
    version="0.0.1",
    openapi_url="/openapi.json"
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=health_router,
    prefix="/api/v1",
    tags=["health"]
)

app.include_router(
    router=rides_router,
    prefix="/api/v1",
    tags=["rides"]
)

app.include_router(
    router=measurement_stream_router,
    prefix="/api/v1",
    tags=["measurement_stream"]
)

app.include_router(
    router=profiles.router,
    prefix="/api/v1",
    tags=["profiles"],
)

app.include_router(
    router=vehicle.router,
    prefix="/api/v1",
    tags=["vehicle"]
)

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

