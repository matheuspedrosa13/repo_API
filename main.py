# Third-Party Library
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jwt import InvalidSignatureError
from starlette.requests import Request
from src.services.crypto.service import ServiceCrypto
from starlette.responses import PlainTextResponse
# Project
from src.services.router.service import Router

from src.routes.route_users.route import router
from src.routes.route_api.route import router
from src.routes.route_catch.route import router

# from src.routes.batalha.route import router

instance_service_crypto = ServiceCrypto()

app = FastAPI(title='pokemon')

app.include_router(Router.get_router())

@app.middleware("http")
async def inteceptacao(request, call_next):
    test_json = request.url
    test_json2 = str(test_json)
    test_json3 = test_json2.find("/docs")
    test_openapi = test_json2.find("/openapi.json")

    if test_json3 != -1 or test_openapi != -1:
        response = await call_next(request)
        return response

    test = request.headers
    test3 = test.values()
    test4 = test.keys()
    try:
        posicao = list(test4).index("token-jwt")
    except:
        return PlainTextResponse("Senha incorreta ou falta token")

    jwt = test3[posicao]

    print(posicao)

    print(
        'Interceptou chegada...'
    )
    if instance_service_crypto.confirm_jwt(jwt) == True:
        print(
            'Interceptou volta'
        )
        str(jwt)

        response = await call_next(request)
        print(jwt)
        print(response)
        return response
    else:
        return PlainTextResponse("Não tem permissão")


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
