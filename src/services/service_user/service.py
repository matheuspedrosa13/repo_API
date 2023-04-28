from src.repositories.repo_user.repository import RepoUser
from src.services.crypto.service import ServiceCrypto


class UserService:
    def __init__(self):
        self.repo_instance = RepoUser()
        self.crypto_instance = ServiceCrypto()

    def search_users(self, token_jwt):
        if self.crypto_instance.confirm_jwt(token_jwt):
            result = self.repo_instance.search_users_active()
            return result
        else:
            return False

    def soft_delete(self, id_user: str, token_jwt):
        if self.crypto_instance.confirm_jwt(token_jwt):
            return self.repo_instance.soft_delete(id_user)
        else:
            return False

    def active_user(self, id_user: str, token_jwt):
        if self.crypto_instance.confirm_jwt(token_jwt):
            return self.repo_instance.active_user(id_user)
        else:
            return False

    def update_user(self, id_user: str, column, value, token_jwt):
        if self.crypto_instance.confirm_jwt(token_jwt):
            return self.repo_instance.update_user(id_user, column, value)
        else:
            return False

    def pagination_users(self, page, page_size, token_jwt):
        if self.crypto_instance.confirm_jwt(token_jwt):
            return self.repo_instance.pagination(page, page_size)
        else:
            return False

