# .venv\Scripts\Activate.ps1

from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from random import shuffle, randint

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

order = list(demo_cards.keys())
shuffle(order)
last_three_cards = []
    
@app.get("/")
def read_root()-> Card:
    while True:
        card = demo_cards[order[randint(0, len(order)-1)]]
        if card.id not in last_three_cards:
            last_three_cards.append(card.id)
            return card

