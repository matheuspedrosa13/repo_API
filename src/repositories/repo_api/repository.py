import requests
from src.domain.pokemon.pokemon_model import Pokemon
from src.infraestructures.poke_api.infraestructure import PokeAPIInfra
from src.infraestructures.mongodb.infraestructure import MongoDBInfra


class RepoAPI:
    def __init__(self):
        self.__client = MongoDBInfra().get_client()
        self.__db = self.__client["pokemonWithJuan"]
        self.__collection = self.__db["pokemon"]
        self.infra = PokeAPIInfra()

    def get_pokemon_from_number(self, number):
        pok = []
        tipos = []
        url = self.infra.get_url()
        url2 = f"{url}/{number}"
        json = requests.get(url2)
        stuff = json.json()
        forms = stuff['forms']
        types = stuff['types']
        nome = forms[0]
        pok.append(nome['name'])
        contador = 0

        while contador < len(types):
            nomType = types[contador]
            tipos.append(nomType['type']['name'])
            contador = contador + 1

        pok.append(tipos)
        print(pok)

    def add_pokemon(self, query: Pokemon):
        col = self.__collection
        dict_user = query.__dict__

        try:
            col.insert_one(dict_user.copy())
            return dict_user
        except Exception as error:
            print(error)
            return "Pokemon não inserido"

    def give_doc(self, param: int):
        filter_number = {"number": int(param)}
        projection = {"_id": 0}
        doc = self.__collection.find_one(filter_number, projection)
        return doc

    def get_url(self):
        url = self.infra.get_url()
        return url

    def pagination(self, page, page_size):
        offSet = page_size * page - page_size
        url = self.infra.get_url()

        every_poke = []

        url2 = f'{url}/?limit={page_size}&offset={offSet}'
        json = requests.get(url2).json()

        for x, i in enumerate(json['results']):

            url3 = json['results'][x]["url"]
            url4 = requests.get(url3).json()
            type = []
            number = url4['id']
            forms = url4['forms']
            types = url4['types']
            xp = url4["base_experience"]

            count = 0
            while count < len(types):
                nomType = types[count]
                type.append(nomType['type']['name'])
                count = count + 1

            test = {
                "number": number,
                "name": forms[0]['name'],
                "type": type,
                "xp": xp
            }

            every_poke.append(test)

        return every_poke

RepoAPI().get_pokemon_from_number(12)