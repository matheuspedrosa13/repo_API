from src.services.service_user.service import UserService
from src.services.router.service import Router
from fastapi import Header

router = Router.get_router()
user_service_instance = UserService()


@router.post("/inserirUsers", tags=['Users'])
def insert_user(name: str, email: str, password: str, gender: str, age: int):
    result = user_service_instance.insert_user(name, email, password, gender, age)
    return result


@router.get("/login_trainer", tags=["Users"])
async def login_trainer(email: str, password: str):
    return user_service_instance.login(email, password)
