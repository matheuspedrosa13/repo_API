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
from src.routes.route_users.route import router as users_router
from src.routes.route_api.route import router as api_router
from src.routes.route_catch.route import router as catch_router

# Create instance of ServiceCrypto
instance_service_crypto = ServiceCrypto()

# Create FastAPI app instance
app = FastAPI(title='pokemon')

# Include routers
app.include_router(Router.get_router())
app.include_router(users_router)
app.include_router(api_router)
app.include_router(catch_router)

# Middleware to intercept incoming requests
@app.middleware("http")
async def inteceptacao(request: Request, call_next):
    # Check if requested route is /docs or /openapi.json
    if "/docs" in request.url.path or "/openapi.json" in request.url.path:
        response = await call_next(request)
        return response

    # Retrieve JWT from request headers
    jwt = request.headers.get("token-jwt")

    # Check if JWT is missing or invalid
    if not jwt or not instance_service_crypto.confirm_jwt(jwt):
        return PlainTextResponse("Não tem permissão")

    rota = str(request.url.path)
    print(rota[1:])
    # Print requested route
    print(f"Requested route: {request.url.path}")

    # Call next middleware or route handler
    response = await call_next(request)
    return response

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run app with Uvicorn
if __name__ == "__main__":
    port = 8888
    uvicorn.run(
        app,
        host="localhost",
        port=port,
        access_log=True,
        root_path="/",
    )
