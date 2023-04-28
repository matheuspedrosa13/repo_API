from uuid import uuid4

import requests
from src.domain.pokemon.pokemon_model import Pokemon
from src.repositories.repo_api.repository import RepoAPI


class PokeApiService:
    def __init__(self):
        self.repo_instance = RepoAPI()
        self.url = self.repo_instance.get_url()

    # FUNÇÕES PARA ENCURTAMENTO DE CÓDIGO:
    @staticmethod
    def add_new_attack(list_of_attacks: list, nome) -> None:
        ability = {
            "ability": {
                "name": nome,
            }
        }

        list_of_attacks.append(ability)

    def get_pokemon(self, number: int):
        url = f"{self.url}/{number}"
        dic = requests.get(url)
        stuff = dic.json()

        return stuff

    def treat_attacks(self, start_list: list, attack_list: list):
        if len(attack_list) == 1:
            start_list.append(attack_list[0])
            self.add_new_attack(start_list, "punch")
            self.add_new_attack(start_list, "kick")
        elif len(attack_list) == 2:
            start_list.append(attack_list[0])
            start_list.append(attack_list[1])
            self.add_new_attack(start_list, "punch")
        elif len(attack_list) >= 3:
            start_list.append(attack_list[0])
            start_list.append(attack_list[1])
            start_list.append(attack_list[2])
        else:
            self.add_new_attack(start_list, "scratch")
            self.add_new_attack(start_list, "punch")
            self.add_new_attack(start_list, "kick")

    @staticmethod
    def return_attack(attack: list, index):
        return attack[index]

    def treat_json(self, number, pok: dict):

        pokemon = self.get_pokemon(number)

        typeA = []
        forms = pokemon['forms']
        types = pokemon['types']
        name = forms[0]
        xp = pokemon["base_experience"]
        attack: list = []
        abilities = pokemon['abilities']

        self.treat_attacks(attack, abilities)

        print(self.return_attack(attack, 0),
              self.return_attack(attack, 1),
              self.return_attack(attack, 2))

        count = 0
        while count < len(types):
            nomType = types[count]
            typeA.append(nomType['type']['name'])
            count = count + 1

        pok["number"] = number
        pok["name"] = name['name']
        pok["type"] = typeA
        pok["xp"] = xp
        pok["attacks"] = attack

    def get_poke_num(self, number):
        return_doc = RepoAPI().give_doc(number)
        return return_doc

    # FUNÇÕES PARA ROTAS:
    def insert_poke(self, number):
        unique_id = str(uuid4())

        return_doc = RepoAPI().give_doc(number)

        print(return_doc)
        if return_doc is None:
            pok = {
                "id_pok": unique_id,
                "number": int,
                "name": str,
                "type": list,
                "xp": int,
                "attacks": list
            }
            self.treat_json(number, pok)
            pok_model = Pokemon(**pok)
            result = self.repo_instance.add_pokemon(pok_model)

            return result

        else:
            return "Pokemon já adicionado no banco"

    def pagination(self, page, page_size):
        result = self.repo_instance.pagination(page, page_size)
        return result
