from uuid import uuid4

from pymongo import ReturnDocument

from src.domain.user.userModel import User
from src.infraestructures.mongodb.infraestructure import MongoDBInfra


class RepoUser:
    def __init__(self):
        self.__client = MongoDBInfra().get_client()
        self.__db = self.__client['pokemonWithJuan']
        self.__collection = self.__db['user']
        self.__collection_adm = self.__db.get_collection("adm")

    def insert_user(self, query: User):
        col = self.__collection
        dict_user = query.__dict__

        try:
            col.insert_one(dict_user.copy())
            return dict_user
        except Exception as error:
            print(error)
            return "Usuário não inserido"

    def give_doc(self, param):
        filter_email = {"email": param}
        doc = self.__collection.find_one(filter_email)
        return doc

    def give_doc_user(self, param):
        filter_id = {"id_user": param}
        doc = self.__collection.find_one(filter_id)
        return doc

    def validate_email_trainer(self, email):
        if self.__collection.find_one({"email": email}):
            return True
        else:
            return False

    def password_trainer(self, email):
        trainer = self.__collection.find_one({"email": email})
        return trainer['password']
