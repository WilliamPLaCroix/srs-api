from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import os

# app imports
from app.core.settings import settings
from app.db.database import Base, engine
from app.db import models

# Routers (domain-level)
from app.modules.cards.router import router as cards_router
from app.modules.decks.router import router as decks_router
from app.modules.reviews.router import router as reviews_router


# -------------------------------------------------
# LIFESPAN (startup / shutdown hooks)
# -------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown (placeholder for now)
    # e.g. close pools, flush queues, etc.


# -------------------------------------------------
# APP
# -------------------------------------------------
app = FastAPI(
    title="Spaced Repetition Flashcards API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/",
    redoc_url="/redoc",
)


# -------------------------------------------------
# ROUTER REGISTRATION
# -------------------------------------------------
app.include_router(cards_router, prefix="/cards", tags=["cards"])
app.include_router(decks_router, prefix="/decks", tags=["decks"])
app.include_router(reviews_router, prefix="/reviews", tags=["reviews"])


# -------------------------------------------------
# ROOT (API health, not UI logic)
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "service": settings.service_name,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "env": settings.environment,
    }


# -------------------------------------------------
# HEALTH CHECK (useful for CI/CD + deployments)
# -------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":

    uvicorn.run("app.main:app",
                host="0.0.0.0",
                port=8000,
                log_level="info",
                reload=True)