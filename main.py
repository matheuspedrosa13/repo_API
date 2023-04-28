# Third-Party Library
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.router.service import Router

from src.routes.route_users.route import router
from src.routes.route_crypto.route import router

app = FastAPI(title='pokemon')

app.include_router(Router.get_router())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = 9999
    uvicorn.run(
        app,
        host="localhost",
        port=port,
        access_log=True,
        root_path="/",
    )
