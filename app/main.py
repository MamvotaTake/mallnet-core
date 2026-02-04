from fastapi import FastAPI
from app.database.init_db import init_db
from app.api.v1.api import api_router

app = FastAPI(title="MallNet Core")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def health():
    return {"status": "ok"}
