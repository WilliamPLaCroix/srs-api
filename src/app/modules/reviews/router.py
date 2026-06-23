import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.reviews.repository import ReviewRepository
from app.modules.reviews.schemas import DeckScore, ReviewCreate, ReviewRead
from app.modules.reviews.services import ReviewService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> ReviewService:
    logger.debug("get_service called: Session=%s", type(db))
    return ReviewService(ReviewRepository(db))


@router.post("/", response_model=ReviewRead)
def create_review(payload: ReviewCreate, service: ReviewService = Depends(get_service)):
    logger.debug("create_review endpoint called: card_id=%s rating=%s", getattr(payload, "card_id", None), getattr(payload, "rating", None))
    try:
        review = service.create_review(payload.card_id, payload.rating)
        logger.info("Review created via endpoint: id=%s card_id=%s rating=%s", getattr(review, "id", None), payload.card_id, payload.rating)
        return review
    except ValueError as e:
        logger.warning("create_review bad request: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in create_review")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/deck/{deck_id}", response_model=DeckScore)
def get_deck_score(deck_id: int, service: ReviewService = Depends(get_service)):
    logger.debug("get_deck_score endpoint called: deck_id=%s", deck_id)
    try:
        result = service.compute_deck_score(deck_id)
        logger.info("Deck score returned via endpoint: deck_id=%s average_score=%s review_count=%s", result.get("deck_id"), result.get("average_score"), result.get("review_count"))
        return result
    except Exception:
        logger.exception("Unexpected error in get_deck_score: deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error")