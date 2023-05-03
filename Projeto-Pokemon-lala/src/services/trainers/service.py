from src.repositories.trainer.repository import RepositoryRegisteredTrainers
from src.services.crypto.service import ServiceCrypto


class ServiceTrainers:
    repository_register = RepositoryRegisteredTrainers()
    service_crypto = ServiceCrypto()

    @classmethod
    def sign(cls, name, email, password, gender):
        name = name.title()
        if gender == "M" or gender == "Diniz":

            password_encrypto = cls.service_crypto.encrypting(password)

            new_user = {
                "name": name,
                "email": email,
                "password": password_encrypto,
                "genre": gender,
                "adm": False
            }

            result = cls.repository_register.sign_trainer(new_user)
            return result
        else:
            return False

    @classmethod
    def login(cls, email, password):
        password_encrypto = cls.service_crypto.encrypting(password)
        result_email = cls.repository_register.validate_email_trainer(email)
        if result_email:
            result_password = cls.repository_register.password_trainer(email)
            result = cls.service_crypto.create_jwt(
                cls.service_crypto.descrypting(result_password),
                cls.service_crypto.descrypting(password_encrypto))
            return result
        else:
            return "email incorreto"

    @classmethod
    def update(cls, user, column, new_value):
        result = cls.repository_register.update_trainer(user, column, new_value)
        return result

    @classmethod
    def soft_delete(cls, user, token_jwt):
        if cls.confirm_jwt(token_jwt):
            result = cls.repository_register.soft_delete(user)
            return result
        else:
            return False

    @classmethod
    def search_trainer(cls, trainer, token_jwt):
        if cls.confirm_jwt(token_jwt):
            result = cls.repository_register.search_trainer(trainer)
            return result
        else:
            return False

    @classmethod
    def confirm_jwt(cls, token_jwt):
        result = cls.service_crypto.confirm_jwt(token_jwt)
        return result
