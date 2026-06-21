# .venv\Scripts\Activate.ps1
# fastapi dev (to launch the server)

from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

# app imports
from app.services.cards import get_card_by_id

app = FastAPI()

class Card(BaseModel):
    id: int
    front: str
    back: str

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

@app.get("/api/data")
async def get_data() -> Card:
    while True:
        card = demo_cards[order[randint(0, len(order)-1)]]
        if card.id not in last_three_cards:
            last_three_cards.append(card.id)
            return card

@app.get("/all_cards")
def read_all_cards(skip: str = "-1", limit: int = 5) -> list[Card]:
    query_cards = demo_cards
    # skip card id if skip is provided
    skip_list = skip.split("-") if skip != "-1" else []
    if skip_list:
        for skip_id in skip_list:
            query_cards.pop(int(skip_id), None)
    # limit the number of cards returned if limit is provided
    if limit != -1:
        query_cards = dict(list(query_cards.items())[:limit])
    return list(query_cards.values())

@app.get("/cards/{card_id}")
def read_card(card_id: int) -> Card | None:
    if card_id not in set(order):
        return error_card
    return demo_cards.get(card_id)

@app.get("/cards/random")
def read_random_card() -> Card:
    return demo_cards[order[0]]

@app.get("/cards/db")
def read_card_db(card_id: int) -> Card | None:
    return get_card_by_id(card_id)