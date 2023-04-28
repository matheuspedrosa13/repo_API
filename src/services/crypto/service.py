import base64
import datetime
import jwt
import requests
from src.repositories.base_mongo.repository import RepositoryBaseMongo
from src.repositories.repo_user.repository import RepoUser


class ServiceCrypto:
    repository_base_mongo = RepositoryBaseMongo()
    repository_register = RepoUser()

    @classmethod
    def encrypting(cls, password):
        try:
            password_utf_8 = ServiceCrypto().utf_8(password)
        except:
            password_utf_8 = password
        public_key = str(cls.repository_base_mongo.get_public_key())
        private_key = str(cls.repository_base_mongo.get_private_key())

        password_crypto = ""

        for letter in password_utf_8:
            value = ord(letter)
            value_cripto = value ^ ord(private_key[0])
            value_cripto = value_cripto ^ ord(public_key[0])
            password_crypto += chr(value_cripto)

        return password_crypto

    @classmethod
    def descrypting(cls, password_crypto):
        public_key = str(cls.repository_base_mongo.get_public_key())
        private_key = str(cls.repository_base_mongo.get_private_key())
        password_descrypto = ""
        for letter in password_crypto:
            value = ord(letter)
            value_cripto = value ^ ord(public_key[0])
            value_cripto = value_cripto ^ ord(private_key[0])
            password_descrypto += chr(value_cripto)
        # return base64.b64encode(password_descrypto.encode('utf-8'))
        return password_descrypto

    @classmethod
    def create_jwt(cls, password_cripto, password):
        if password_cripto == password:
            today = datetime.date.today()
            date = (datetime.date(year=today.year,
                                  month=today.month,
                                  day=today.day + 1).isoformat())
            stuff = {
                "signature": cls.encrypting(
                    cls.repository_base_mongo.get_signature()),
                "expiration_date": cls.encrypting(date)
            }
            return jwt.encode(stuff, key=cls.repository_base_mongo.get_jwt_key(), algorithm="HS256")
        else:
            return "senha incorreta"

    @classmethod
    def confirm_jwt(cls, jwt):
        # TODO fazer requisição pro outro projeto na rota /confirm_jwt
        a = requests.get(f'http://localhost:9999/confirm_jwt?jwt={jwt}')
        if (a.content).decode("utf-8") == 'true':
            return True
        else:
            return False
        # TODO tudo abaixo dessa linha "morre"
        #
        # jwt = ServiceCrypto.descrypting_jwt(token_jwt)
        # true_signature = ServiceCrypto.descrypting(cls.repository_base_mongo.get_signature())
        # expiration = ServiceCrypto.isExpiration(jwt['expiration_date'])
        # if expiration.days > 0:
        #     if jwt['signature'] == true_signature:
        #         return True
        #     else:
        #         return False
        # else:
        #     return "Login Expirado =["

    @classmethod
    def descrypting_jwt(cls, token_jwt):
        return jwt.decode(token_jwt, cls.repository_base_mongo.get_jwt_key(), algorithms="HS256")

    @classmethod
    def isExpiration(cls, date_jwt):
        today = datetime.date.today()
        true_date = cls.descrypting(date_jwt).split('-')
        result = datetime.datetime(int(true_date[0]), int(true_date[1]), int(true_date[2])) - datetime.datetime(
            today.year, today.month, today.day)
        return result

    @classmethod
    def utf_8(cls, password):
        return (base64.b64decode(password.encode('ascii'))).decode('ascii')

print(ServiceCrypto.confirm_jwt('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWduYXR1cmUiOiJzb3licWFqaWV7Ylx1MDA3Zm5pMjg_PmNsbmp8fnxcdTAwN2Z7bGk_OFx1MDA3ZjhQOFtfOTBHPTtQRyY_JElcdTAwY2M5aVAmPSIsImV4cGlyYXRpb25fZGF0ZSI6Ijk7OTgmOz8mOTIifQ.Hc0L6a8wnXtGUKiMrd5_hax1xbFr9K4W8h7TpzIW7vQa'))