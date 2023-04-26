from src.services.serviceCatch.service import CatchService
from src.services.router.service import Router

router = Router.get_router()
catch_service_instance = CatchService()


@router.post("/capturarPokemons", tags=['Captura'])
def captura(user_id, nickname, poke_num):
    return catch_service_instance.catch_poke(user_id, nickname, poke_num)
