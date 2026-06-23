import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_review_service
from app.db.session import get_session
from app.modules.reviews.schemas import DeckScore, ReviewCreate, ReviewRead

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=ReviewRead)
def create_review(payload: ReviewCreate, session: Session = Depends(get_session)):  # noqa: B008
    logger.debug(
        "create_review endpoint called: card_id=%s rating=%s",
        getattr(payload, "card_id", None),
        getattr(payload, "rating", None),
    )
    service = get_review_service(session)
    try:
        review = service.create_review(payload.card_id, payload.rating)
        logger.info(
            "Review created via endpoint: id=%s card_id=%s rating=%s",
            getattr(review, "id", None),
            payload.card_id,
            payload.rating,
        )
        return review
    except ValueError as err:
        logger.warning("create_review bad request: %s", err)
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error in create_review")
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.get("/deck/{deck_id}", response_model=DeckScore)
def get_deck_score(deck_id: int, session: Session = Depends(get_session)):  # noqa: B008
    logger.debug("get_deck_score endpoint called: deck_id=%s", deck_id)
    service = get_review_service(session)
    try:
        result = service.compute_deck_score(deck_id)
        logger.info(
            "Deck score returned via endpoint: deck_id=%s average_score=%s review_count=%s",
            result.get("deck_id"),
            result.get("average_score"),
            result.get("review_count"),
        )
        return result
    except Exception as err:
        logger.exception("Unexpected error in get_deck_score: deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err
