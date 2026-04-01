from fastapi import FastAPI
from routers import orders
from database import init_db
from middleware.logging import logging_middleware

app = FastAPI(title="Book API")
app.middleware("http")(logging_middleware)

app.include_router(orders.router)


@app.get("/")
async def root():
    return {"status": "ok", "docs": "/docs"}

@app.on_event("startup")
async def on_startup():
    await init_db()