from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.modules.cards.schemas import CardCreate, CardRead
from app.modules.cards.repository import CardRepository
from app.modules.cards.services import CardService


router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> CardService:
    repo = CardRepository(db)
    return CardService(repo)


@router.post("/", response_model=CardRead)
def create_card(payload: CardCreate, service: CardService = Depends(get_service)):
    try:
        return service.create_card(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{card_id}", response_model=CardRead)
def get_card(card_id: int, service: CardService = Depends(get_service)):
    try:
        return service.get_card(card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/deck/{deck_id}", response_model=list[CardRead])
def get_cards(deck_id: int, service: CardService = Depends(get_service)):
    return service.get_cards_for_deck(deck_id)

@router.delete("/{card_id}")
def delete_card(card_id: int, service: CardService = Depends(get_service)):
    try:
        service.delete_card(card_id)
        return {"detail": "Card deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))