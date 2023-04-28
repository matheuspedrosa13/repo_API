from src.services.crypto.service import ServiceCrypto
from src.services.router.service import Router

router = Router.get_router()
crypto_service_instance = ServiceCrypto()


@router.get("/confirm_jwt", tags=["Crypto"])
async def confirm_jwt(jwt: str):
    return crypto_service_instance.confirm_jwt(jwt)
