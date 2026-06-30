from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers

from app.api.accounts import router as account_router
from app.api.transactions import router as transaction_router

app = FastAPI(title=settings.APP_NAME)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(transaction_router)


@app.get("/")
async def root():
    return {
        "message": "Banking API is running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
    }