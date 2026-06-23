import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_deck_service
from app.db.session import get_session
from app.modules.decks.schemas import DeckCreate, DeckRead, DeckWithCards

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=DeckRead)
def create_deck(payload: DeckCreate, session: Session = Depends(get_session)):  # noqa: B008
    logger.debug("create_deck endpoint called: name_present=%s", bool(getattr(payload, "name", "")))
    service = get_deck_service(session)
    try:
        deck = service.create_deck(payload.name)
        logger.info(
            "Deck created via endpoint: id=%s name=%s",
            getattr(deck, "id", None),
            getattr(deck, "name", None),
        )
        return deck
    except ValueError as err:
        logger.warning("create_deck bad request: %s", err)
        raise HTTPException(status_code=400, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error in create_deck")
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.get("/{deck_id}", response_model=DeckRead)
def get_deck(deck_id: int, session: Session = Depends(get_session)):  # noqa: B008
    logger.debug("get_deck endpoint called: deck_id=%s", deck_id)
    service = get_deck_service(session)
    try:
        deck = service.get_deck(deck_id)
        logger.info("Deck fetched via endpoint: deck_id=%s", deck_id)
        return deck
    except ValueError as err:
        logger.info("get_deck not found: deck_id=%s", deck_id)
        raise HTTPException(status_code=404, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error in get_deck: deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.get("/{deck_id}/full", response_model=DeckWithCards)
def get_deck_full(deck_id: int, session: Session = Depends(get_session)):  # noqa: B008
    logger.debug("get_deck_full endpoint called: deck_id=%s", deck_id)
    service = get_deck_service(session)
    try:
        result = service.get_deck_with_cards(deck_id)
        logger.info("Deck with cards returned via endpoint: deck_id=%s", deck_id)
        return result
    except ValueError as err:
        logger.info("get_deck_full not found: deck_id=%s", deck_id)
        raise HTTPException(status_code=404, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error in get_deck_full: deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err


@router.delete("/{deck_id}")
def delete_deck(deck_id: int, session: Session = Depends(get_session)):  # noqa: B008
    logger.debug("delete_deck endpoint called: deck_id=%s", deck_id)
    service = get_deck_service(session)
    try:
        result = service.delete_deck(deck_id)
        logger.info("Deck deleted via endpoint: deck_id=%s", deck_id)
        return result
    except ValueError as err:
        logger.info("delete_deck not found: deck_id=%s", deck_id)
        raise HTTPException(status_code=404, detail=str(err)) from err
    except Exception as err:
        logger.exception("Unexpected error deleting deck_id=%s", deck_id)
        raise HTTPException(status_code=500, detail="Internal server error") from err
