from pydantic import BaseModel


class Battle(BaseModel):
    ataque: int
    id_battle: str
    id_user: str
    id_poke_winner: str
