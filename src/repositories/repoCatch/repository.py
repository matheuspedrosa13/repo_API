from src.infraestructures.mongodb.infraestructure import MongoDBInfra
from src.domain.catch.catchModel import Catch


class RepoCatch:

    def __init__(self):
        self.client = MongoDBInfra().get_client()
        self.__database = self.client.get_database('pokemonWithJuan')
        self.__collectionCap = self.__database.get_collection('catch')

    def catch_pok(self, query: Catch):
        # try:
        dict_cap = query.__dict__
        self.__collectionCap.insert_one(dict_cap.copy())
    #     return "aaaa"
    # # except Exception as error:
    #     return error
