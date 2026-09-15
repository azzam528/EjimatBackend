from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import health, penduduk
from app.routers.kartu_keluarga import (
    router as kartu_keluarga_router
)
# pyrefly: ignore [missing-import]
from app.routers.anggota_keluarga import (
    router as anggota_keluarga_router
)
from app.routers.duplicate_detection import (
    router as duplicate_detection_router
)
from app.routers.dusun import router as dusun_router
from app.routers.rw import router as rw_router
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Basic CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix=f"{settings.API_PREFIX}/health", tags=["health"])
app.include_router(penduduk.router, prefix=f"{settings.API_PREFIX}/penduduk", tags=["penduduk"])
app.include_router(kartu_keluarga_router)
app.include_router(anggota_keluarga_router)
app.include_router(duplicate_detection_router)
app.include_router(dusun_router)
app.include_router(rw_router)


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API. Visit /docs for documentation."}
