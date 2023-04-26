# Third-Party Library
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from src.services.crypto.service import ServiceCrypto

# Project
from src.services.router.service import Router

from src.routes.routeUsers.route import router
from src.routes.routeAPI.route import router
from src.routes.routeCatch.route import router
# from src.routes.batalha.route import router

instance_service_crypto = ServiceCrypto()

app = FastAPI(title='pokemon')

app.include_router(Router.get_router())


@app.middleware("http")
async def inteceptacao(request, call_next):
    from starlette.datastructures import Headers
    # if request.method == 'post':
    test = request.headers
    test2 = type(test)
    test3 = test.values()
    test4 = test.keys()
    jwt = test3[6]

    try:
        instance_service_crypto.confirm_jwt(jwt)
    except:
        return "deu ruim"
    print(
        'Interceptou chegada...'
    )
    response = await call_next(request)

    print(
        'Interceptou volta'
    )
    print(response)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = 8888
    uvicorn.run(
        app,
        host="localhost",
        port=port,
        access_log=True,
        root_path="/",
    )
