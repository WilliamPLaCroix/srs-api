import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_card_service
from app.db.session import get_session
from app.modules.cards.repository import CardRepository
from app.modules.cards.schemas import CardCreate, CardRead
from app.modules.cards.services import CardService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=CardRead)
def create_card(payload: CardCreate, session: Session = Depends(get_session)):
    logger.debug(
        "create_card endpoint called: deck_id=%s front_present=%s back_present=%s",
        getattr(payload, "deck_id", None),
        bool(getattr(payload, "front", None)),
        bool(getattr(payload, "back", None)),
    )
    service = get_card_service(session)
    try:
        card = service.create_card(payload)
        logger.info(
            "Card created via endpoint: id=%s deck_id=%s",
            getattr(card, "id", None),
            getattr(card, "deck_id", None),
        )
        return card
    except ValueError as err:
        logger.warning("create_card bad request: %s", err)
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error in create_card")
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.get("/{card_id}", response_model=CardRead)
def get_card(card_id: int, session: Session = Depends(get_session)):
    logger.debug("get_card endpoint called: card_id=%s", card_id)
    service = get_card_service(session)
    try:
        card = service.get_card(card_id)
        logger.info("Card fetched via endpoint: card_id=%s", card_id)
        return card
    except ValueError as err:
        logger.info("get_card not found: card_id=%s", card_id)
        raise HTTPException(status_code=404, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error in get_card: card_id=%s", card_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.get("/deck/{deck_id}", response_model=list[CardRead])
def get_cards(deck_id: int, session: Session = Depends(get_session)):
    logger.debug("get_cards endpoint called: deck_id=%s", deck_id)
    service = get_card_service(session)
    try:
        cards = service.get_cards_for_deck(deck_id)
        logger.info("Returning %s cards for deck_id=%s", len(cards), deck_id)
        return cards
    except Exception as err:
        logger.exception("Unexpected error listing cards for deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.delete("/{card_id}")
def delete_card(card_id: int, session: Session = Depends(get_session)):
    logger.debug("delete_card endpoint called: card_id=%s", card_id)
    service = get_card_service(session)
    try:
        service.delete_card(card_id)
        logger.info("Card deleted via endpoint: card_id=%s", card_id)
        return {"detail": "Card deleted"}
    except ValueError as err:
        logger.info("delete_card not found: card_id=%s", card_id)
        raise HTTPException(status_code=404, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error deleting card_id=%s", card_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err
