from fastapi import FastAPI
from app.routers import drivers, clients, health

app = FastAPI(title="Trips API")

app.include_router(drivers.router)
app.include_router(clients.router)
app.include_router(health.router)
