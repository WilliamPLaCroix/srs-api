from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.reviews.schemas import ReviewCreate, ReviewRead, DeckScore
from app.modules.reviews.repository import ReviewRepository
from app.modules.reviews.services import ReviewService


router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> ReviewService:
    return ReviewService(ReviewRepository(db))


@router.post("/", response_model=ReviewRead)
def create_review(payload: ReviewCreate, service: ReviewService = Depends(get_service)):
    try:
        return service.create_review(payload.card_id, payload.rating)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/deck/{deck_id}", response_model=DeckScore)
def get_deck_score(deck_id: int, service: ReviewService = Depends(get_service)):
    return service.compute_deck_score(deck_id)