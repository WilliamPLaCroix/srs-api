# .venv\Scripts\Activate.ps1
# fastapi dev (to launch the server)

from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from random import shuffle, randint
from fastapi.responses import HTMLResponse

app = FastAPI()

class Card(BaseModel):
    id: int
    front: str
    back: str

demo_cards = {
    0: Card(id=0, front="id0: This is a simple sentence", back="(Notes and translation)"),
    1: Card(id=1, front="id1: This could be a more complex sentence", back="(Notes and translation)"),
    2: Card(id=2, front="id2: This is a sentence with multiple clauses, which makes it more interesting.", back="(Notes and translation)"),
    3: Card(id=3, front="id3: This is a sentence with an idiom, which can be tricky to understand.", back="(Notes and translation)"),
    4: Card(id=4, front="id4: This is a sentence with a cultural reference, which may require additional context to fully grasp.", back="(Notes and translation)"),
    5: Card(id=5, front="id5: This is a sentence with a pun, which can be difficult to translate accurately.", back="(Notes and translation)"),
    6: Card(id=6, front="id6: This is a sentence with a metaphor, which can be open to interpretation.", back="(Notes and translation)"),
    7: Card(id=7, front="id7: This is a sentence with a simile, which can be used to create vivid imagery.", back="(Notes and translation)"),
    8: Card(id=8, front="id8: This is a sentence with a rhetorical question, which can be used to make a point or provoke thought.", back="(Notes and translation)"),
    9: Card(id=9, front="id9: This is a sentence with a hyperbole, which can be used for emphasis or humor.", back="(Notes and translation)"),
}
error_card = Card(id=-1, front="Error: Invalid card ID", back="Please provide a valid card ID.")

order = list(demo_cards.keys())
shuffle(order)
last_three_cards = []

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