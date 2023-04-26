from src.services.serviceAPI.service import PokeApiService
from src.services.router.service import Router

router = Router.get_router()


@router.get("/procurarPokemonsPorNumero", tags=['Pokemon'])
def get_pokemon(num):
    return PokeApiService().get_poke_num(num)


@router.post("/adicionarPokemonsPorNumero", tags=['Pokemon'])
def add_pok(num):
    pokemon_service_instance = PokeApiService()
    result = pokemon_service_instance.insert_poke(num)
    return result


@router.get("/paginarPokemon", tags=['Pokemon'])
def pagination(page: int, page_size: int):
    pag = PokeApiService().pagination(page, page_size)
    return pag
