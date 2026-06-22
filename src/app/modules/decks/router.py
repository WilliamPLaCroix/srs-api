from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.decks.schemas import DeckCreate, DeckRead, DeckWithCards
from app.modules.decks.repository import DeckRepository
from app.modules.decks.services import DeckService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> DeckService:
    return DeckService(DeckRepository(db))


@router.post("/", response_model=DeckRead)
def create_deck(payload: DeckCreate, service: DeckService = Depends(get_service)):
    try:
        return service.create_deck(payload.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{deck_id}", response_model=DeckRead)
def get_deck(deck_id: int, service: DeckService = Depends(get_service)):
    try:
        return service.get_deck(deck_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{deck_id}/full", response_model=DeckWithCards)
def get_deck_full(deck_id: int, service: DeckService = Depends(get_service)):
    try:
        return service.get_deck_with_cards(deck_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{deck_id}")
def delete_deck(deck_id: int, service: DeckService = Depends(get_service)):
    try:
        return service.delete_deck(deck_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))