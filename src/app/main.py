# .venv\Scripts\Activate.ps1
# fastapi dev (to launch the server)

from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from random import choice

# app imports
from app.modules.cards.services import get_card_by_id
from app.db.models import Card
from app.db.database import SessionLocal
from app.modules.cards.create import CardCreate

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Tester</title>
    </head>
    <body>
        <h1>API Test Interface</h1>
        <button onclick="fetchData()">Select random card</button>
        <pre id="result">Click the button to fetch card data</pre>
        
        <script>
            async function fetchData() {
                const result = document.getElementById('result');
                result.textContent = 'Loading...';
                
                try {
                    const response = await fetch('/api/data');
                    const data = await response.json();
                    result.textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    result.textContent = 'Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    """

# TODO this function needs to be changed to pull from the database instead of the demo cards OR "/api/data" should be moved to get("/cards")
@app.get("/api/data")
async def get_data() -> Card:
    while True:
        card = demo_cards[order[randint(0, len(order)-1)]]
        if card.id not in last_three_cards:
            last_three_cards.append(card.id)
            return card

@app.get("/cards")
def get_all_cards():
    db = SessionLocal()

    cards = db.execute(select(Card)).scalars().all()
    return cards

@app.get("/cards/{card_id}")
def get_card(card_id: int):
    db = SessionLocal()

    card = db.get(Card, card_id)

    if not card:
        return {"error": "card not found"}

    return card

@app.get("/cards/random")
def get_random_card():
    db = SessionLocal()

    cards = db.execute(select(Card)).scalars().all()

    if not cards:
        return {"error": "no cards in database"}

    return choice(cards)

@app.get("/cards/db")
def read_card_db(card_id: int) -> Card | None:
    return get_card_by_id(card_id)

@app.post("/cards")
def create_card(card: CardCreate):
    db = SessionLocal()

    new_card = Card(front=card.front, back=card.back)

    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return new_card