from src.services.service_user.service import UserService
from src.services.router.service import Router
from fastapi import Header

router = Router.get_router()
user_service_instance = UserService()


@router.get("/verUsersAtivos", tags=['Users'])
def search_activated_users(token_jwt: str = Header(...)):
    return user_service_instance.search_users(token_jwt)


@router.get("/paginacaoUser", tags=['Users'])
def pagination_user(page: int, page_size: int, token_jwt: str = Header(...)):
    return user_service_instance.pagination_users(page, page_size, token_jwt)


@router.put("/desativarUser", tags=['Users'])
def soft_delete(id_user: str, token_jwt: str = Header(...)):
    return user_service_instance.soft_delete(id_user, token_jwt)


@router.put("/ativarUser", tags=['Users'])
def active_user(id_user: str, token_jwt: str = Header(...)):
    return user_service_instance.active_user(id_user, token_jwt)


@router.put("/alterarUser", tags=['Users'])
def alter_user(id_user: str, column, value, token_jwt: str = Header(...)):
    if column == "age_user":
        int(value)
        return user_service_instance.update_user(id_user, column, value, token_jwt)

    return user_service_instance.update_user(id_user, column, value, token_jwt)
