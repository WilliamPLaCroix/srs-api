import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.health import router as health_router
from app.core.logging import setup_logging

# Core
from app.core.middleware import RequestContextMiddleware
from app.core.settings import settings

# Database
from app.db.base import Base
from app.db.engine import engine

# from app.db.registry import *  # noqa: F403, F401
# Routers (domain-level)
from app.modules.cards.router import router as cards_router
from app.modules.decks.router import router as decks_router
from app.modules.reviews.router import router as reviews_router


# -------------------------------------------------
# LIFESPAN (startup / shutdown hooks)
# -------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown (placeholder for now)
    # e.g. close pools, flush queues, etc.


logger = logging.getLogger(__name__)


# -------------------------------------------------
# APP
# -------------------------------------------------
app = FastAPI(
    title="Spaced Repetition Flashcards API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(RequestContextMiddleware)

# -------------------------------------------------
# ROUTER REGISTRATION
# -------------------------------------------------
app.include_router(cards_router, prefix="/cards", tags=["cards"])
app.include_router(decks_router, prefix="/decks", tags=["decks"])
app.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
app.include_router(health_router, prefix="/core", tags=["core"])

# print("IMPORT cards_router")
# from app.modules.cards.router import router as cards_router

# print(cards_router.routes)

# print("INCLUDING cards_router")
# app.include_router(cards_router, prefix="/cards")

# print("APP ROUTES AFTER CARDS:", app.routes)

# print("IMPORT decks_router")
# from app.modules.decks.router import router as decks_router

# print(decks_router.routes)

# print("INCLUDING decks_router")
# app.include_router(decks_router, prefix="/decks")

# print("APP ROUTES AFTER DECKS:", app.routes)

# print("IMPORT reviews_router")
# from app.modules.reviews.router import router as reviews_router

# print(reviews_router.routes)

# print("INCLUDING reviews_router")
# app.include_router(reviews_router, prefix="/reviews")

# print("APP ROUTES AFTER REVIEWS:", app.routes)


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


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)


if __name__ == "__main__":
    main()
