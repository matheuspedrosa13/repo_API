from pydantic import BaseModel


class Pokemon(BaseModel):
    id_pok: str
    number: int
    name: str
    type: list
    xp: int
    attacks: list
