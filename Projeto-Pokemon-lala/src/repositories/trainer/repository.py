from uuid import uuid4
import base64

from src.infraestructures.mongodb.infraestructure import MongoDBInfra
from src.domain.models.trainer.model import UserModel


class RepositoryRegisteredTrainers:
    def __init__(self):
        self.cluster = MongoDBInfra.get_client()
        self.data_base = self.cluster.get_database("site_pokemons")
        self.colection_registered = self.data_base.get_collection("registered")
        self.colection_adm = self.data_base.get_collection("adm")

    def sign_trainer(self, new_user):
        try:
            new_user: UserModel
            if self.colection_registered.find_one({"email": new_user["email"]}):
                return "Está conta já existe"
            else:
                new_user["unique_id"] = str(uuid4())
                new_user["active"] = True

                self.colection_registered.insert_one(new_user)
                return "registrado!"
        except:
            return False

    def validate_email_trainer(self, email):
        if self.colection_registered.find_one({"email": email}):
            return True
        else:
            return False

    def password_trainer(self, email):
        trainer = self.colection_registered.find_one({"email": email})
        return trainer['password']

    def update_trainer(self, user, column, new_value):
        try:
            user_dict = self.search_trainer(user)
            if self.colection_registered.find_one({"name": new_value}) \
                    or self.colection_registered.find_one({"email": new_value}):
                return "O nome ou o email já está sendo usado"
            else:
                self.colection_registered.update_one({"email": user_dict["email"]}, {"$set": {column: new_value}})
                return "Usuario alterado!"
        except:
            return False

    def soft_delete(self, user):
        try:
            user_dict = self.search_trainer(user)
            self.colection_registered.find_one_and_update({"email": user_dict["email"]},
                                                          {"$set": {"active": False if user_dict["active"] else True}})
            return "Usuario Excluido!"
        except:
            return False

    def search_trainer(self, trainer):
        try:
            user_dict = self.colection_registered.find_one({"email": trainer}, {'unique_id': 0, '_id': 0})
            return user_dict
        except:
            return False
