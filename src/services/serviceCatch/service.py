from src.repositories.repoAPI.repository import RepoAPI
from src.repositories.repoCatch.repository import RepoCatch
from src.domain.catch.catchModel import Catch
from src.services.serviceAPI.service import PokeApiService
from uuid import uuid4

from src.repositories.repoUser.repository import RepoUser


class CatchService:

    @classmethod
    def catch_poke(cls, user_id, nickname, poke_num):

        verification = RepoUser().give_doc_user(user_id)

        if verification is not None:
            pokemon = PokeApiService().get_poke_num(poke_num)

            if pokemon is None:
                PokeApiService().insert_poke(poke_num)

            pokemon = PokeApiService().get_poke_num(poke_num)
            number = pokemon["number"]
            specie = pokemon["name"]
            types = pokemon["type"]
            xp = pokemon["xp"]

            unique_id = str(uuid4())

            catch_dict = {
                "id_catch": unique_id,
                "num_pok": number,
                "id_user": user_id,
                "nick": nickname,
                "pokemon": specie,
                "types": types,
                "xp": xp
            }

            catch_model = Catch(**catch_dict)

            RepoCatch().catch_pok(catch_model)

            return "Inserido no banco!"
        else:
            return "Usuário não existe!"


