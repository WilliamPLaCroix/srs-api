# .venv\Scripts\Activate.ps1
# fastapi dev (to launch the server)

from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from random import choice
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html

# app imports
from app.modules.cards.services import get_card_by_id
from app.db.models import Card
from app.db.database import SessionLocal
from app.modules.cards.create import create_card

app = FastAPI(docs_url="/",title="Spaced Repetition Flashcard API")

# @app.get("/")
# async def root():
#     return RedirectResponse(url="/#")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom API UI")

# # TODO this function needs to be changed to pull from the database instead of the demo cards OR "/api/data" should be moved to get("/cards")
# @app.get("/api/data")
# async def get_data() -> Card:
#     while True:
#         card = demo_cards[order[randint(0, len(order)-1)]]
#         if card.id not in last_three_cards:
#             last_three_cards.append(card.id)
#             return card

@app.get("/cards", tags=["Cards"])
def get_all_cards():
    db = SessionLocal()

    cards = db.execute(select(Card)).scalars().all()
    return cards

@app.get("/cards/{card_id}", tags=["Cards"])
def get_card(card_id: int):
    db = SessionLocal()

    card = db.get(Card, card_id)

    if not card:
        return {"error": "card not found"}

    return card

@app.get("/cards/random", tags=["Cards"])
def get_random_card():
    db = SessionLocal()

    cards = db.execute(select(Card)).scalars().all()

    if not cards:
        return {"error": "no cards in database"}

    return choice(cards)

# @app.get("/cards/db")
# def read_card_db(card_id: int) -> Card | None:
#     return get_card_by_id(card_id)

# @app.post("/cards")
# def create_card():
#     db = SessionLocal()

#     new_card = create_card(front=card.front, back=card.back)

#     db.add(new_card)
#     db.commit()
#     db.refresh(new_card)

#     return new_card


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)