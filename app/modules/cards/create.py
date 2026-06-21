from pydantic import BaseModel
from .schemas import CardSchema

# use kwargs to create a card in the database
def create_card(**kwargs):

    return CardSchema(**kwargs)