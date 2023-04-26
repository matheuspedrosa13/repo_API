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

    def search_users_active(self):
        status = {"status": True}
        docs = self.__collection.find(status, {'_id': 0})
        result = []
        for x in docs:
            try:
                User(**x)
                result.append(x)

            except Exception as error:
                print(error)
                return f"Coisa errada no banco {x=}"

        return result

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

    def soft_delete(self, id: str):
        filter_id = {"id_user": id}
        doc = self.__collection.find_one(filter_id)

        if doc["status"]:
            doc = self.__collection.find_one_and_update(filter_id, {'$set': {'status': False}}, return_document=True)
            return "Usuário desativado"
        else:
            return "Não foi possível desativar usuário"

    def active_user(self, id):
        id1 = {"id_user": id}
        doc = self.__collection.find_one(id1)
        if not doc["status"]:
            self.__collection.find_one_and_update(id1, {'$set': {'status': True}}, return_document=True)
            return "Treinador ativado com sucesso!"
        else:
            return "Treinador já ativo!"

    def update_user(self, id, column, value):
        filter_id = {"id_user": id}

        update = {"$set": {column: value}}

        projection = {
            "_id": False
        }

        updated_document = self.__collection.find_one_and_update(filter_id, update, projection=projection,
                                                                 return_document=ReturnDocument.AFTER)
        return updated_document

    def pagination(self, page, page_size):
        projection = {
            "_id": 0
        }
        skip_valor = page - 1
        if skip_valor <= -1 or page <= 0 or page_size <= 0:
            return "Páginas ou a quantidade de treinadores por pagina não podem ser 0 ou menor que 0"
        else:
            user = self.__collection.find({}, projection).skip(skip_valor * page_size).limit(page_size)
            return list(user)

    def validate_email_trainer(self, email):
        if self.__collection.find_one({"email": email}):
            return True
        else:
            return False

    def password_trainer(self, email):
        trainer = self.__collection.find_one({"email": email})
        return trainer['password']

