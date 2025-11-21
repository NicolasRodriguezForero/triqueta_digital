"""
Main FastAPI application.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

from app.core.config import settings
from app.services.popularity_job import recalculate_popularity_job
from app.services.recommendation_service import recommendation_service

logger = logging.getLogger(__name__)

# Initialize scheduler
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting application...")
    
    # Schedule daily popularity recalculation at 2 AM
    scheduler.add_job(
        recalculate_popularity_job,
        'cron',
        hour=2,
        minute=0,
        id='recalculate_popularity',
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started - popularity job scheduled for 2 AM daily")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    scheduler.shutdown()
    await recommendation_service.close()
    logger.info("Application shutdown complete")


# Create FastAPI app with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
# Parse CORS origins from comma-separated string
cors_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Triqueta Digital API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include API routers
from app.api.v1 import auth, users, activities, favorites, recommendations, admin

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(activities.router, prefix="/api/v1")
app.include_router(favorites.router, prefix="/api/v1/favoritos", tags=["favoritos"])
app.include_router(recommendations.router, prefix="/api/v1/recomendaciones", tags=["recomendaciones"])
app.include_router(admin.router, prefix="/api/v1")

