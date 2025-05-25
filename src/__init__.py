from fastapi import FastAPI
from src.routes.bikes import bikes_router
from src.routes.messages import messages_router
from src.routes.users import users_router
from src.routes.rides import rides_router
from src.config import Settings
from contextlib import asynccontextmanager
from src.config import settings
from src.db import init_db

# lifespan code

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()

    yield

def create_app():
    app = FastAPI(
        description="A REST API for managing bike rides, users, and messages.",
        title="On Wheels API",
        version=settings.VERSION,
        lifespan=lifespan
    )
    app.include_router(bikes_router)
    app.include_router(messages_router)
    app.include_router(rides_router)
    app.include_router(users_router)

    return app


app = create_app()
