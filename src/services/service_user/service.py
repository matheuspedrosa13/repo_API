from uuid import uuid4
from src.domain.user.userModel import User
from src.repositories.repo_user.repository import RepoUser
from src.services.crypto.service import ServiceCrypto


class UserService:
    def __init__(self):
        self.repo_instance = RepoUser()
        self.crypto_instance = ServiceCrypto()

    def insert_user(self, name: str, email: str, password: str, gender: str, age: int):
        unique_id = str(uuid4())

        return_doc = RepoUser().give_doc(email)
        password_encrypto = self.crypto_instance.encrypting(password)

        if return_doc is None:
            user_dict = {
                "id_user": unique_id,
                "name_user": name,
                "age_user": age,
                "gender": gender,
                "email": email,
                "password": password_encrypto,
                "status": True
            }
            user_model = User(**user_dict)
            result = self.repo_instance.insert_user(user_model)
            return result
        else:
            return "Já utilizaram esse email em outro usuário"

    def login(self, email, password):
        password_encrypto = self.crypto_instance.encrypting(password)
        result_email = self.repo_instance.validate_email_trainer(email)
        if result_email:
            result_password = self.repo_instance.password_trainer(email)
            result = self.crypto_instance.create_jwt(
                self.crypto_instance.descrypting(result_password),
                self.crypto_instance.descrypting(password_encrypto))
            return result
        else:
            return "email incorreto"
