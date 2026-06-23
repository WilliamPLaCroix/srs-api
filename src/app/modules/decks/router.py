import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.decks.repository import DeckRepository
from app.modules.decks.schemas import DeckCreate, DeckRead, DeckWithCards
from app.modules.decks.services import DeckService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> DeckService:
    logger.debug("get_service called: Session=%s", type(db))
    return DeckService(DeckRepository(db))


@router.post("/", response_model=DeckRead)
def create_deck(payload: DeckCreate, service: DeckService = Depends(get_service)):
    logger.debug("create_deck endpoint called: name_present=%s", bool(getattr(payload, "name", "")))
    try:
        deck = service.create_deck(payload.name)
        logger.info("Deck created via endpoint: id=%s name=%s", getattr(deck, "id", None), getattr(deck, "name", None))
        return deck
    except ValueError as e:
        logger.warning("create_deck bad request: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in create_deck")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{deck_id}", response_model=DeckRead)
def get_deck(deck_id: int, service: DeckService = Depends(get_service)):
    logger.debug("get_deck endpoint called: deck_id=%s", deck_id)
    try:
        deck = service.get_deck(deck_id)
        logger.info("Deck fetched via endpoint: deck_id=%s", deck_id)
        return deck
    except ValueError as e:
        logger.info("get_deck not found: deck_id=%s", deck_id)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in get_deck: deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{deck_id}/full", response_model=DeckWithCards)
def get_deck_full(deck_id: int, service: DeckService = Depends(get_service)):
    logger.debug("get_deck_full endpoint called: deck_id=%s", deck_id)
    try:
        result = service.get_deck_with_cards(deck_id)
        logger.info("Deck with cards returned via endpoint: deck_id=%s", deck_id)
        return result
    except ValueError as e:
        logger.info("get_deck_full not found: deck_id=%s", deck_id)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.exception("Unexpected error in get_deck_full: deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{deck_id}")
def delete_deck(deck_id: int, service: DeckService = Depends(get_service)):
    logger.debug("delete_deck endpoint called: deck_id=%s", deck_id)
    try:
        result = service.delete_deck(deck_id)
        logger.info("Deck deleted via endpoint: deck_id=%s", deck_id)
        return result
    except ValueError as e:
        logger.info("delete_deck not found: deck_id=%s", deck_id)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.exception("Unexpected error deleting deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error")