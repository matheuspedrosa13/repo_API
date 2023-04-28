from pydantic import BaseModel


class Catch(BaseModel):
    id_catch: str
    num_pok: int
    id_user: str
    nick: str
    pokemon: str
    types: list
    xp: int

