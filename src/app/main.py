from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import Base, engine

# Import models so SQLAlchemy registers them
from app.db import models  # noqa: F401

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
    title="Bookwurm API",
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
        "service": "bookwurm",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# -------------------------------------------------
# HEALTH CHECK (useful for CI/CD + deployments)
# -------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}