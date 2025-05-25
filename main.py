from fastapi import FastAPI
from src.routes import users, bikes, rides, messages
from src.db import init_db

app = FastAPI(
    title="On Wheels API",
    description="A REST API for managing bike rides, users, and messages.",
    version="v1",
    docs_url="/docs"
)

app.include_router(users.router)
app.include_router(bikes.router)
app.include_router(rides.router)
app.include_router(messages.router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API On Wheels 🚀"}
