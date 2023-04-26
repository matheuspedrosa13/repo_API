import uvicorn
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from src.services.app.service import RouterService

import src.routes.trainer.route
stuff = RouterService.get_router()
app = FastAPI(title="Pokemon")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.include_router(
    stuff
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = 8000
    uvicorn.run(
        app,
        host="localhost",
        port=port,
        access_log=True,
        root_path="/"
    )
