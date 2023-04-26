from src.domain.models.trainer.model import UserModel
from src.services.app.service import RouterService
from src.services.trainers.service import ServiceTrainers
from fastapi import Header

app = RouterService.get_router()


@app.post("/sign_trainer", tags=["trainer"])
async def sign_new_trainer(name: str, email: str, password: str, gender: str):
    return ServiceTrainers.sign(name, email, password, gender)


@app.get("/login_trainer", tags=["trainer"])
async def login_trainer(email: str, password: str):
    return ServiceTrainers.login(email, password)


@app.put("/alter_trainer", tags=["trainer"])
async def alter_trainer(trainer: str, column: str, new_value: str, token_jwt: str = Header(...)):
    return ServiceTrainers.update(trainer, column, new_value, token_jwt)


@app.put("/delete_trainer", tags=["trainer"])
async def delete_trainer(trainer: str, token_jwt: str = Header(...)):
    return ServiceTrainers.soft_delete(trainer, token_jwt)


@app.get("/search_trainer", tags=["trainer"])
async def search_trainer(trainer: str, token_jwt: str = Header(...)):
    return ServiceTrainers.search_trainer(trainer, token_jwt)
