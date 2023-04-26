from pydantic import BaseModel


class Xupeta(BaseModel):

    nome: str
    idade: int



my_xupeta_dict: dict = {
    "nome": "x",
    "idade": 1
}

my_xupeta = Xupeta(
    nome="x",
    idade=1
)

print(type(my_xupeta))
